#include <stdio.h>

struct model {
	int states;
	int emissions;
	float* transition;
	float* emission;
	float* initial;
};

#define trans(from,to) (transition[from*states+to])
#define emis(state,obs) (emission[state*states+obs])
#define init(state) (initial[state])

__device__ float par_sum(int state, float *shared, int states) {
	printf("called with state %d of %d\n",state,states);
	int step=1;
	int depth=2;
	do {
		printf("Depth %d Thread %d temp %f states %d\n", depth, state, shared[state], states);
		if (state%depth == 0) {
			printf("Checked Depth %d Thread %d temp %f states %d\n", depth, state, shared[state], states);
			if (state+step < states) {
				// regular case
				// to self add depth far right sibiling
				printf("Summing %f += %f\n",shared[state],shared[state+step]);
				shared[state] += shared[state+step];
			} else {
				printf("Else clause state %d + step %d < states %d\n",state,step,states);
				// loose end case
				// do nothing
				// same as copy from previous
			}
		}
		__syncthreads();
		step = depth;
	} while ((depth*=2) < states);

	printf("Parralel sum %f\n",shared[0]);
	return shared[0];
}
/*
  Takes model and observation sequence of length len and produces
  alfa part of forward-backward algorithm. Normalized for
  numerical stability.
  Assumes alpha is pointer to float array of size m->states * len
  */
// call withc alpha_norm<<grid,block,len*sizeof(int)>>
__global__ void alpha_norm(float* alpha, int states, int emissions, int len, float *transition, float* emission, float *initial, int* obs) {
	int state = blockIdx.x * blockDim.x + threadIdx.x;

	extern __shared__ int s[];
	float *shared = (float *)s;

	if (state >= states) {
		return;
	}

#if 0
	// clear output memory
	for (int i = 0; i < len; i++) {
		alpha[state*len + i] = 0;
	}
#endif

	if (obs[0] > emissions) {
		printf("Observation %d outside model\n",obs[0]);
	}

	printf("Before [%f, %f]\n",alpha[0],alpha[1]);
	// initialize edge case
	shared[state] = init(state) * emis(state,obs[0]);

	// normalize
	alpha[state] = shared[state];
	__syncthreads();
	float sum = par_sum(state, shared, states);
	printf("Sum %f\n",sum);
	alpha[state] /= sum;
	__syncthreads();
	printf("After [%f, %f]\n",alpha[0],alpha[1]);

	printf("initial %d state \n", state);

	// j - observations
	// for each observation sta
	for (int j = 1; j < len - 1; j++) {

		int idx = j * states + state;
		printf("Internal state %d, j %d, idx %d\n",state,j,idx);

		// i - previous state
		// sum for each previous state * transition from previous to current
		sum = 0.f;
		for (int i = 0; i < states; i++) {
			printf("Internal state %d, j %d, i%d\n",state,j,i);
			sum += alpha[states * (j-1) + i] * trans(i,state);
		}

		// normalize
		shared[state]= sum * emis(state,obs[j]);
		alpha[idx] = shared[state];
		__syncthreads();
		sum = par_sum(state, shared, states);
		alpha[idx] /= sum;
		__syncthreads();
	}
	printf("end %d state \n", state);

	__syncthreads();
}

__global__ void beta_norm(float* beta, int states, int emissions, int len, float *transition, float* emission, float *initial, int* obs) {
	int state = blockIdx.x * blockDim.x + threadIdx.x;

	extern __shared__ int s[];
	float *shared = (float *)s;

	if (state >= states) {
		return;
	}

#if 1
	// clear output memory
	for (int i = 0; i < len; i++) {
		beta[state*len + i] = 0;
	}
#endif

	// edge case
	int idx = (len-1) * states + state;
	beta[idx] = 1.f/states;

	// j - observation
	// for each observation from the end
	for (int j = len - 2; j >= 0; j--) {
		int nidx = (j+1) * states + state;
		float sum = 0.f;
		for (int i = 0; i < states; i++) {
			sum += trans(state,i) * emis(state,obs[j+1]) * beta[nidx];
		}
		idx = j * states + state;
		beta[idx] = sum;
		__syncthreads();

		/* shared[state] = beta[idx]; */
		/* __syncthreads(); */
		/* sum = par_sum(state, shared, states); */
		/* beta[idx] /= sum; */

		__syncthreads();
	}

	__syncthreads();
}

