r = getEventListeners(document)['keydown'][0]['listener'];
// function loop() { r.tRex.setDuck(); window.requestAnimationFrame(loop); }
canvas = document.getElementsByTagName("canvas")[0]; //[0];
width = canvas.width;
height = canvas.height;
context = canvas.getContext('2d');

function vectorize(context, width, height) {
	var data = context.getImageData(0, 0, width, height);
	var size = width * height;
	var vector = Array(size);
	for (var i = 0; i < size; i++) {
		var value = data.data[4*i];
		value = value/255.0;
		value += randn_bm()/20.0;
		vector[i] = value;
	}
	return vector;
}

// Standard Normal variate using Box-Muller transform.
// http://stackoverflow.com/questions/25582882/javascript-math-random-normal-distribution-gaussian-bell-curve
function randn_bm() {
    var u = 1 - Math.random(); // Subtraction to flip [0, 1) to (0, 1].
    var v = 1 - Math.random();
    return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
}

function minmax(array) {
	var min = Number.POSITIVE_INFINITY;
	var max = Number.NEGATIVE_INFINITY;
	for (var i = 0; i < array.length; i++) {
		if (array[i] < min) {
			min = array[i];
		}
		if (array[i] > max) {
			max = array[i];
		}
	}
	return [min, max];
}

function sigmoid(x) {
	return 1/(1+Math.exp(-x));
}
function d_sigmoid(x) {
	//var y = sigmoid(x)
	//return y*(1-y);
	return x*(1-x);
}

function Neuron(size) {
	this.size = size;
	this.weights = Array(size);
	for (var i = 0; i < size; i++) {
		this.weights[i] = randn_bm()/100;
	}
}

Neuron.prototype.visualize = function(context, width, height) {
	var data = context.createImageData(width, height);
	var mm = minmax(this.weights);
	var min = mm[0];
	var max = mm[1];
	var delta = 255;
	for (var i = 0; i < height; i++) {
		for (var j = 0; j < width; j++) {
			var index = i * width + j;
			var sign = this.weights[index] > 0 ? 1 : -1;
			var value = (this.weights[index] - min)/max * delta;
			data.data[4*index] =  sign > 0 ? value : 0;
			data.data[4*index+1] = 0; //value;
			data.data[4*index+2] = sign <= 0 ? value : 0;
			data.data[4*index+3] = 255;// value;
		}
	}
	context.putImageData(data, 0, 0);
	return data;
}

Neuron.prototype.forward = function(vector) {
	var out = 0;
	for (var i = 0; i < this.size; i++) {
		out += this.weights[i] * vector[i];
	}
	//console.log(out);
	return sigmoid(out);
}

Neuron.prototype.backward = function(vector, out, exp) {
	var error = exp - out;
	var delta = error * d_sigmoid(out);

	var lerrors = Array(this.size - 1);
	for (var i = 0; i < this.size - 1; i++) {
		lerrors[i] = delta * this.weights[i];
	}

	for (var i = 0; i < this.size; i++) {
		this.weights[i] += vector[i] * delta;
	}

	return lerrors;
}

function forward(vector, out_neuron, neurons) {
	var out_hidden = Array(neurons.length + 1);
	// bias
	out_hidden[neurons.length] = 1.0;

	// forward propagation hidden layer
	for (var i = 0; i < neurons.length; i++) {
		var neuron = neurons[i];
		var score = neuron.forward(vector);
		out_hidden[i] = score;
	}

	// forward out layer
	var out = out_neuron.forward(out_hidden);

	return out;
}

function train(vector, error, out_neuron, neurons) {
	var out_hidden = Array(neurons.length + 1);
	// bias
	out_hidden[neurons.length] = 1.0;

	// forward propagation hidden layer
	for (var i = 0; i < neurons.length; i++) {
		var neuron = neurons[i];
		var score = neuron.forward(vector);
		out_hidden[i] = score;
	}

	// forward out layer
	var out = out_neuron.forward(out_hidden);

	// bacward out layer
	//var error = out * score;
	//var error = score;
	var delta = error * d_sigmoid(out);

	var lerror = Array(out_neuron.size - 1);
	for (var i = 0; i < out_neuron.size - 1; i++) {
		lerror[i] = delta * out_neuron.weights[i];
	}

	// train out neuron
	for (var i = 0; i < out_neuron.size; i++) {
		out_neuron.weights[i] += out_hidden[i] * delta;
	}

	// train hidden
	for (var i = 0; i < neurons.length; i++) {
		var neuron = neurons[i];
		var herror = lerror[i];
		var ldelta = herror * d_sigmoid(out_hidden[i]);
		for (var j = 0; j < neuron.size; j++) {
			neuron.weights[j] += vector[j] * ldelta;
		}
	}

	//console.log(out_hidden);
	//console.log(out);
	return out;
}

hidden_count = 12;
hidden_neurons = Array(hidden_count);
jump_hidden = Array(hidden_count/2);
run_hidden = Array(hidden_count/2);

hidden_canvas = Array(hidden_count);
hidden_context = Array(hidden_count);

jump_neuron = new Neuron(hidden_count/2 + 1);
run_neuron = new Neuron(hidden_count/2 + 1);

jump_neurons = Array(hidden_count/2);
run_neurons = Array(hidden_count/2);

history_length = 60;

function init() {
	var tag = document.getElementById("main-message");
	tag.innerHTML = "";
	//tag.innerHTML = '<div id="dropZone" style="width: 100px; height: 100px; background-color: red"></div>';
	var i = 0;
	for (i = 0; i < hidden_count; i++){
		var canvas = document.createElement("canvas");
		canvas.style = "width: 300px; height: 100px;";
		tag.appendChild(canvas);
		canvas.width = width;
		canvas.height = height;
		var context = canvas.getContext("2d");
		var neuron = new Neuron(width*height);
		hidden_neurons[i] = neuron;
		hidden_context[i]= context;
		hidden_canvas[i] = canvas;
	}
	for (var k = 0; k< hidden_count/2; k++) {
		jump_neurons[k] = new Neuron(hidden_count/2 + 1);
		run_neurons[k] = new Neuron(hidden_count/2 + 1);
	}
	for (var k = 0; k < hidden_count/2; k++) {
		jump_hidden[k] = hidden_neurons[k];
	}
	for (var l = 0; l < hidden_count/2; l++) {
		run_hidden[l] = hidden_neurons[hidden_count/2 + l];
	}
	for (var j = 0; j < history_length; j++) {
		var canvas = document.createElement("canvas");
		canvas.style = "width: 300px; height: 100px;";
		tag.appendChild(canvas);
		canvas.width = width;
		canvas.height = height;
		var context = canvas.getContext("2d");
		hidden_context[i+j+1]= context;
		hidden_canvas[i+j+1] = canvas;
	}
}


function test(count) {
	function and(x,y) {
		if (x==1 && y==1) {
			return 1;
		}
		return 0;
	}
	function xor(x,y) {
		if (x == 0 && y == 1)
			return 1;
		if (x == 1 && y == 0)
			return 1;
		return 0;
	}

	var bool = xor;

	function random_v() {
		var out = Array(3);
		out[2] = 1;
		out[1] = Math.random() > 0.5 ? 1 : 0;
		out[0] = Math.random() > 0.5 ? 1 : 0;
		return out;
	}

	//debugger;
	if (!count) {
		count = 2;
	}
	var neurons = Array(count);
	for (var i = 0; i < count; i++) {
		neurons[i] = new Neuron(3);
	}
	var out_neuron = new Neuron(count+1);


	for (var iters = 0; iters < 100000; iters++) {
		var vector = random_v();
		var out_hidden = Array(count+1);
		out_hidden[count] = 1;
		// forward propagation hidden layer
		for (var i = 0; i < count; i++) {
			var neuron = neurons[i];
			var score = neuron.forward(vector);
			out_hidden[i] = score;
		}

		// forward out layer
		var out = out_neuron.forward(out_hidden);

		// bacward out layer
		var expected = bool(vector[0],vector[1]);

		var error = expected - out;

		var delta = error * d_sigmoid(out);

		if (iters % 1000 == 0) {
			console.log(vector,expected,out,error,delta);
		}

		var lerror = Array(out_neuron.size - 1);
		for (var i = 0; i < out_neuron.size - 1; i++) {
			lerror[i] = delta * out_neuron.weights[i];
		}

		// train out neuron
		for (var i = 0; i < out_neuron.size; i++) {
			out_neuron.weights[i] += out_hidden[i] * delta;
		}

		// train hidden
		for (var i = 0; i < count; i++) {
			var neuron = neurons[i];
			var herror = lerror[i];
			var ldelta = herror * d_sigmoid(out_hidden[i]);
			for (var j = 0; j < neuron.size; j++) {
				neuron.weights[j] += vector[j] * ldelta;
			}
		}
	}

	console.log(out_neuron.weights); //, neurons[0].weights, neurons[1].weights, neurons[2].weights, neurons[3].weights);
	for (var i = 0; i < count; i++) {
		console.log(neurons[i].weights);
	}
}

function visualize() {
	for (var i = 0; i < hidden_neurons.length; i++) {
		hidden_neurons[i].visualize(hidden_context[i],width, height);
	}
}

function drawvector(context, vector) {
	var data = context.createImageData(width, height);
	var mm = minmax(vector);
	var min = mm[0];
	var max = mm[1];
	var delta = 255;
	for (var i = 0; i < height; i++) {
		for (var j = 0; j < width; j++) {
			var index = i * width + j;
			var value = (vector[index] - min)/max * delta;
			data.data[4*index] = value;
			data.data[4*index+1] = value;
			data.data[4*index+2] = value;
			data.data[4*index+3] = 255;//value;
		}
	}
	context.putImageData(data, 0, 0);
}

init();
visualize();

function vector_diff(first, second) {
	var out = Array(first.length);
	for (var i = 0; i < first.length; i++) {
		out[i] = first[i] - second[i];
	}
	return out;
}

function merge_vectors(first, second) {
	var out = Array(first.length);
	for (var i = 0; i < height; i++) {
		for (var j = 0; j < width/2; j++) {
			var index = i * width + j;
			out[index] = first[index];
		}
	}
	for (var i = 0; i < height; i++) {
		for (var j = 0; j < width/2; j++) {
			var index = i * width + j;
			out[index + width/2] = second[index];
		}
	}
	return out;
}


function merge_history(vector, history_vector) {
	var high = 5;
	var line = height - high;
	//line = 11;
	var len = 5;
	//debugger;
	for (var i = 0; i < history_vector.length; i++) {
		var hist = history_vector[i];
		var action = hist[1];
		if (action == 1) {

			for (var j = 0; j < high; j++) {
				var index = (line - j) * width + len * i;
				for (var k = 0; k < len; k++) {
					vector[index + k] = 1;
				}

				index = (line + j) * width + len * i;
				for (var k = 0; k < len; k++) {
					vector[index + k] = 0;
				}
			}

		} else {

			for (var j = 0; j < high; j++) {
				var index = (line - j) * width + len * i;
				for (var k = 0; k < len; k++) {
					vector[index + k] = 0;
				}

				index = (line + j) * width + len * i;
				for (var k = 0; k < len; k++) {
					vector[index + k] = 1;
				}
			}

		}
	}
	return vector;
}


v = vectorize(context, width, height);
previous_vector = null;
n = hidden_neurons[0];

fps = 20;
history_length = 2 * fps;
history_vector = [];

// for (var i = 0; i < history_length; i++) {
// 	var vector = vectorize(context, width, height);
// 	history_vector.push(vector);
// }

r.old_update = r.update;
iter = 0;
jumps = 0;
runs = 0;
pause = false;
last_run_score = 0;
last_jump_score = 0;

uparr = { keyCode: 38, type: 'keydown', preventDefault: function() {} };
downarr = { keyCode: 40, type: 'keyup', preventDefault: function() {} };
r.update = function() {
	//var old_vector = history_vector.shift();
	//history_vector.push(vector);

	//console.log("update");
	r.old_update();
	if (pause) {
		//debugger;
	}
	if (!r.crashed) { //} && !r.paused && r.playing) {
		var current_vector = vectorize(context, width, height);
		if (!previous_vector) {
			previous_vector = current_vector;
		}

		var vector = merge_vectors(current_vector, previous_vector);
		vector = merge_history(vector, history_vector);
		previous_vector = current_vector;

		iter++;
		// train(old_vector, 0.1);
		// debugger;
		/*
		if (iter % 600 == 0) {

			visualize();
			console.log(iter, jumps, runs, jumps/(jumps+runs), "jump", last_jump_score, "run", last_run_score);
			console.log("jumps", jump_neuron.weights);
			console.log("run ", run_neuron.weights);
		}
		*/
		//debugger;
		//var jump_scores = new Float32Array(hidden_count/2);
		//var run_scores = new Float32Array(hidden_count/2);

		var jump_neuron = jump_neurons[0];
		var run_neuron = run_neurons[0];
		var jump_score = 0;
		var run_score = 0;
		for (var i = 0; i < hidden_count/2; i++) {
			var l_jump_neuron = jump_neurons[i];
			var l_run_neuron = run_neurons[i];
			var l_jump_score = forward(vector, l_jump_neuron, jump_hidden);
			var l_run_score = forward(vector, l_run_neuron, run_hidden);
			if (l_jump_score > jump_score) {
				jump_score = l_jump_score;
				jump_neuron = l_jump_neuron;
			}
			if (l_run_score > run_score) {
				run_score = l_run_score;
				run_neuron = l_run_neuron;
			}

		}


		last_jump_score = jump_score;
		last_run_score = run_score;

		var rand = Math.random() * (jump_score + run_score);

		var neuron = jump_neuron;

		//var rand = Math.random();
		//var action =  rand < score ? 1 : 0;
		if (rand < jump_score) {
			action = 1;
			score = jump_score;
			neuron = jump_neuron;
		} else {
			action = 0;
			score = run_score;
			neuron = run_neuron;
		}

		if (action == 1) {
			//console.log("jump", rand, score);
			//debugger;
			r.onKeyDown(uparr);
			r.onKeyUp(uparr);
			//r.tRex.startJump(r.currentSpeed);
			jumps += 1;

		} else {
			//r.onKeyDown(downarr);
			//r.onKeyUp(downarr);
			runs += 1;

			//console.log("dont jump", rand, score);

		}
		history_vector.push( [vector, action, score, neuron] );

		if (history_vector.length > history_length) {
			var v = history_vector.shift();
			var action = v[1];
			var score = v[2];
			var rate = 0.01;
			var neuron = v[3];
			var error = rate*(1 - score); // 0.001
			if (action == 1) {
				//debugger;
				train(v[0], error, neuron, jump_hidden);
			} else {
				train(v[0], error, neuron, run_hidden);
			}
		}
	} else {
		previous_vector = null;
		if (iter % 1000 == 0) {
			console.clear();
		}
		visualize();

			//console.log("jumps", jump_neuron.weights);
			//console.log("run ", run_neuron.weights);

		//iter = 0;
		//console.log("crashed", r.crashed, r.paused, r.playing);
		for (var i = 0; i < history_vector.length; i++) {
			//console.log("train history", i)
			var v = history_vector.pop();
			var action = v[1];
			var score = v[2];
			var rate = 0.01;
			var neuron = v[3];
			var error = rate*(0 - score); //-0.01;

			//console.log(action == 1 ? "jump" : "run", score, neuron.weights);
			//debugger;
			if (action == 1) {
				train(v[0], error, neuron, jump_hidden);
			} else {
				train(v[0], error, neuron, run_hidden);
			}
			//debugger;
			drawvector(hidden_context[hidden_count + 1 + i], v[0]);
			pause = true;
		}
		console.log(iter, jumps, runs, jumps/(jumps+runs), "jump", last_jump_score, "run", last_run_score);
		for (var i = 0; i < run_neurons.length; i++) {
			console.log("run neuron", i, run_neurons[i].weights);
		}
		for (var i = 0; i < jump_neurons.length; i++) {
			console.log("jump neuron", i, jump_neurons[i].weights);
		}
		jumps = 0;
		runs = 0;

		r.onKeyDown(uparr);
		r.onKeyUp(uparr);
		r.restart();
		r.onKeyDown(uparr);
		r.onKeyUp(uparr);

	}

}

// hidden_neurons[0].visualize(context, width, height);
// for(var i = 0; i < 10; i++) { train(v,0.1); visualize() }
/*
function loop() {
	r.tRex.startJump(r.currentSpeed);
	// keep 2s of history
	// if still in game
	// pop last history, train it with score = 1 (one frame lived)
	// if game over
	// pop whole history, train it with -1
	// assume last 2s of actions were wrong



	window.requestAnimationFrame(loop);
}
loop();
*/
