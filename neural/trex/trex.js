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
		vector[i] = data.data[4*i]/255.0;
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
		this.weights[i] = randn_bm()/10;
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
			var value = (this.weights[index] - min)/max * delta;
			data.data[4*index] = value;
			data.data[4*index+1] = value;
			data.data[4*index+2] = value;
			data.data[4*index+3] = value;
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

function train(vector, score) {
	var out_hidden = Array(hidden_count + 1);
	// bias
	out_hidden[hidden_count] = 1.0;

	// forward propagation hidden layer
	for (var i = 0; i < hidden_count; i++) {
		var neuron = hidden_neurons[i];
		var score = neuron.forward(vector);
		out_hidden[i] = score;
	}

	// forward out layer
	var out = out_neuron.forward(out_hidden);

	// bacward out layer
	var error = out * score;
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
	for (var i = 0; i < hidden_count; i++) {
		var neuron = hidden_neurons[i];
		var herror = lerror[i];
		var ldelta = herror * d_sigmoid(out_hidden[i]);
		for (var j = 0; j < neuron.size; j++) {
			neuron.weights[i] += vector[i] * ldelta;
		}
	}

	//console.log(out_hidden);
	//console.log(out);
	return out;
}

hidden_count = 4;
hidden_neurons = Array(hidden_count);

hidden_canvas = Array(hidden_count);
hidden_context = Array(hidden_count);

out_neuron = new Neuron(hidden_count + 1);

function init() {
	var tag = document.getElementById("main-message");
	tag.innerHTML = "";

	for (var i = 0; i < hidden_count; i++){
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
	for (var i = 0; i < hidden_count; i++) {
		hidden_neurons[i].visualize(hidden_context[i],width, height);
	}
}

init();
visualize();

v = vectorize(context, width, height);
n = hidden_neurons[0];

fps = 60;
history_length = 2 * fps;
history_vector = [];

for (var i = 0; i < history_length; i++) {
	var vector = vectorize(context, width, height);
	history_vector.push(vector);
}

r.old_update = r.update;
iter = 0;
r.update = function() {
	var vector = vectorize(context, width, height);
	var old_vector = history_vector.shift();
	history_vector.push(vector);
	//console.log("update");
	r.old_update();
	if (!r.crashed) {
		iter++;
		train(old_vector, 0.1);
		if (iter >= 60) {
			visualize();
		}
	} else {

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
