struct model {
	int states;
	int emissions;
	float* transitions;
	float* emissions;
	float* initial
}

__global__ alpha_norm(struct model* model, int *observations) {
}

__global__ beta_norm() {
}

__global__ ksi_gamma() {
}

__global__ baum_welch() {
}
