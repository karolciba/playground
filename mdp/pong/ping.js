var animate = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || function (callback) {
        window.setTimeout(callback, 1000 / 60)
    };

game = null;

function Paddle(x, y, width, height) {
  this.x = x;
  this.y = y;
  this.sx = 0;
  this.sy = 0;
  this.pickups = 0;
  this.width = width;
  this.height = height;
}

Paddle.prototype.render = function (context) {
    context.fillStyle = "#0000FF";
    context.fillRect(this.x, this.y, this.width, this.height);
    var i = document.getElementById("debug");
    i.innerHTML += "" + this.x + " " + this.y + " " + this.width + " " +this.height + "<br/>";
}

Paddle.prototype.update = function(game) {
  this.x += this.sx;
  this.y += this.sy;
  if (this.y < 0) {
    this.y = 0;
    this.sy = 0;
  } else if (this.y + this.height > game.height) {
    this.y = game.height - this.height;
    this.sy = 0;
  }
}

Paddle.prototype.move_up = function() {
  this.sy = 4;
}

Paddle.prototype.move_down = function() {
  this.sy = -4;
}

Paddle.prototype.stop = function() {
  this.sy = 0;
}

function Player(paddle) {
  this.paddle = paddle;
}

Player.prototype.update = function(game) {
  if (game.keys[40]) {
    this.paddle.move_up();
  } else if (game.keys[38]) {
    this.paddle.move_down();
  } else {
    this.paddle.stop();
  }

  this.paddle.update(game);
}

Player.prototype.after = function(game) {
}

function Reflex(paddle) {
  this.paddle = paddle;
}

Reflex.prototype.update = function(game) {
  if (game.ball.y > this.paddle.y && game.ball.y < this.paddle.y + this.paddle.height) {
    this.paddle.stop();
  } else if (game.ball.y < this.paddle.y) {
    this.paddle.move_down();
  } else {
    this.paddle.move_up();
  }
}

Reflex.prototype.after = function(game) {
}

function Markov(paddle) {
  this.paddle = paddle;
  this.pickups = 0;
  this.q_states = {}
  this.pre_state = null;
  this.post_state = null;
  this.action = 'stop';
  this.actions = ['stop', 'up', 'down'];
  this.alpha = 0.3;
  this.factor = 0.5;
  this.persev = 0.75;
  this.discount = 0.9;
  this.pairs_history = [];

  this.teacher_counter = 100000;
}

Markov.prototype.state_hash = function(game) {
  var pos_step = 10;
  var speed_step = 4;
  var ball_x = Math.round(game.ball.x*pos_step/game.width);
  var ball_y = Math.round(game.ball.y*pos_step/game.height);
  var ball_sx = Math.round(game.ball.sx*speed_step/4);
  var ball_sy = Math.round(game.ball.sy*speed_step/4);
  var player_y = Math.round(game.player.paddle.y*pos_step/game.height);
  var opponent_y = Math.round(game.opponent.paddle.y*pos_step/game.height);
  var key = [ball_x, ball_y, ball_sx, ball_sy, player_y, opponent_y ]

  return key;
}

Markov.prototype.update = function(game) {
    var i = document.getElementById("debug");

  this.pre_state = this.state_hash(game);

  if (this.teacher_counter > 0) {
    i.innerHTML += "<br/>teacher " + this.teacher_counter;

    this.teacher_counter -= 1;
    if (game.ball.y > this.paddle.y && game.ball.y < this.paddle.y + this.paddle.height) {
      this.paddle.stop();
      this.action = 'stop';
    } else if (game.ball.y < this.paddle.y) {
      this.paddle.move_down();
      this.action = 'down';
    } else {
      this.paddle.move_up();
      this.action = 'up';
    }

    return;
  }

  // select random action
  if (this.factor > Math.random()) {
    var item = 'stop';
    if (this.persev > Math.random()) {
      // stick to previous actuion
      item = this.action;
      i.innerHTML += "<br/>prandom " + item;
    } else {
      item = this.actions[Math.floor(Math.random()*this.actions.length)];
      i.innerHTML += "<br/>rrandom " + item;
      this.action = item;
    }
    if (item == 'stop') {
      this.paddle.stop();
    } else if (item == 'down') {
      this.paddle.move_down();
    } else {
      this.paddle.move_up();
    }
    i.innerHTML += "<br/>random " + item;
  } else {
    var best_value = -1;
    var best_action = 'stop';
    for (var key in this.actions) {
      var action = this.actions[key];
      var value = this.get_q_value(this.pre_state, action);
      if (value > best_value) {
        best_value = value;
        best_action = action;
      }
    }

    i.innerHTML += "<br/>best " + best_action + " " + best_value;
    var item = best_action;
    this.action = item;
    if (item == 'stop') {
      this.paddle.stop();
    } else if (item == 'down') {
      this.paddle.move_down();
    } else {
      this.paddle.move_up();
    }
  }


  // if (game.ball.y > this.paddle.y && game.ball.y < this.paddle.y + this.paddle.height) {
  //   this.paddle.stop();
  //   this.action = 'stop';
  // } else if (game.ball.y < this.paddle.y) {
  //   this.paddle.move_down();
  //   this.action = 'down';
  // } else {
  //   this.paddle.move_up();
  //   this.action = 'up';
  // }

  // this.pre_state = this.state_hash(game);
  // console.log(this.state_hash(game));
}

Markov.prototype.get_q_value = function(state, action) {
  var pair = [state, this.action];
  if (! this.q_states[pair]) {
    return 0;
    // this.q_states[pair] = 0;
  }
  return this.q_states[pair];
}

Markov.prototype.get_value = function(state) {
  var best_value = -1;
  var best_action = 'stop';
  for (var key in this.actions) {
    var action = this.actions[key];
    var value = this.get_q_value(state, action);
    if (value > best_value) {
      best_value = value;
      best_action = action;
    }
  }
  return best_value;
}

Markov.prototype.after = function(game) {
  var pickups_delta = this.paddle.pickups - this.pickups;
  this.pickups = this.paddle.pickups;
  // var reward = game.living + 1000 * pickups_delta;
  var reward = 1000 * pickups_delta;
  if (reward != 0) {
    // debugger;
  }
  var discount = 1;
  this.post_state = this.state_hash(game);
  var pair = [this.pre_state, this.action];

  if (""+this.pairs_history[0] != ""+pair) {
    this.pairs_history.unshift(pair);
    if (this.pairs_history.length > 100) {
      this.pairs_history.pop();
    }
  } else {
    // debugger;
  }
  // if (! this.q_states[pair]) {
  //   this.q_states[pair] = 0;
  // }
  // this.q_states[pair] = this.alpha * reward + (1-this.alpha)*this.q_states[pair];
  var p = this.get_value(this.post_state);
  var score = this.alpha * (reward + discount * p)
    + (1-this.alpha)*this.get_q_value(this.pre_state, this.action);
  if (score > 0) {
    this.q_states[pair] = score;

    for (var i = 0; i < this.pairs_history.length; i++) {
      var ppair = this.pairs_history[i];
      score = (1 - this.discount) * score;
      var previous = this.q_states[ppair];
      if (!previous) {
        previous = 0;
      }
      this.q_states[ppair] = this.alpha * previous + (1 - this.alpha) * score;
    }

  }
  // debugger;
}

function Ball() {
  this.x = 0;
  this.y = 0;
  this.width = 10;
  this.height = 10;
  this.sx = 0;
  this.sy = 0;
}

Ball.prototype.render = function (context) {
    context.fillStyle = "#0000FF";
    context.fillRect(this.x, this.y, this.width, this.height);
    // context.beginPath();
    // context.arc(this.x, this.y, 5, 2 * Math.PI, false);
    // context.fillStyle = "#000000";
    // context.fill();
}

Ball.prototype.update = function(game) {
  this.x += this.sx;
  this.y += this.sy;

  // end of board collision
  // if (this.x < 0 || this.x > game.width) {
  //   this.reset();
  // }
  
  // wall collision
  if (this.y < 0) {
    this.y = 0;
    this.sy = -this.sy;
  } else if (this.y + this.height > game.height) {
    this.y = game.height - this.height;
    this.sy = -this.sy;
  // paddle collision
  } else if (this.x < game.player.paddle.x + game.player.paddle.width
            && this.y + this.height > game.player.paddle.y
            && this.y < game.player.paddle.y + game.player.paddle.height) {
    this.sx = -this.sx;
    // this.sy = -this.sy;
    this.x = game.player.paddle.x + game.player.paddle.width;
    this.sy += game.player.paddle.sy / 2;
    game.player.paddle.pickups += 1;
    // this.sx += game.player.paddle.sy;
  } else if (this.x + this.width > game.opponent.paddle.x
            && this.y + this.height > game.opponent.paddle.y
            && this.y < game.opponent.paddle.y + game.opponent.paddle.height) {
    this.sx = -this.sx;
    // this.sy = -this.sy;
    this.x = game.opponent.paddle.x - this.width;
    this.sy += game.opponent.paddle.sy / 2;
    game.opponent.paddle.pickups += 1;
    // this.sx -= game.opponent.paddle.sy;
  } else if (this.x < 0) {
    game.opponent_wins += 1;
    game.living = 0;
    this.reset();
  } else if (this.x + this.width > game.width) {
    game.player_wins += 1;
    game.living = 0;
    this.reset();
  }

  if (this.sy == 0) {
    this.sy = Math.round(Math.random()*3.99) - 2;
  }

    var i = document.getElementById("debug");
    i.innerHTML += "<br/>ball sx" + this.sx + " ball sy" + this.sy + "<br/>";

}

Ball.prototype.reset = function() {
  this.x = 300;
  this.y = 200;
  // this.sx = Math.round(1 + Math.random()*3);
  this.sx = 4;
  if (Math.random() > 0.5) {
    this.sx = -this.sx;
  }
  this.sy = Math.round(1 + Math.random()*3);
  if (Math.random() > 0.5) {
    this.sy = -this.sy;
  }
}

function Game() {
  // this.info = document.createElement("span");
  // this.canvas = document.createElement("canvas");
  this.info = document.getElementById("span");
  this.canvas = document.getElementById("canvas");
  this.width = 600;
  this.height = 400;
  this.canvas.width = 600;
  this.canvas.height = 400;
  this.context = this.canvas.getContext('2d');
  this.keys = {}
  this.living = 0;

  this.ball = new Ball();
  this.ball.reset();
  // this.player = new Player(10, 175, 10, 50);
  this.p_paddle = new Paddle(10, 175, 10, 50);
  this.o_paddle = new Paddle(580, 175, 10, 50);
  this.player = new Markov(this.p_paddle);
  this.opponent = new Reflex(this.o_paddle);

  this.player_wins = 0;
  this.opponent_wins = 0;


  self = this;
  window.addEventListener("keydown", function (event) {
      self.keys[event.keyCode] = true;
  });

  window.addEventListener("keyup", function (event) {
      self.keys[event.keyCode] = false;
  });
}

Game.prototype.reset = function() {
  this.ball.x = 200;
  this.ball.y = 300;
  this.ball.sx = Math.round(Math.random()*3.99);
  this.ball.sy = Math.round(Math.random()*3.99) - 2;
}

Game.prototype.render = function() {
  this.context.fillStyle = "#222222";
  this.context.fillRect(0,0, this.width, this.height);

  this.ball.render(this.context);
  this.p_paddle.render(this.context);
  this.o_paddle.render(this.context);

  this.info.innerHTML = "Player " + this.player_wins
    + "<br /> Opponent "+ this.opponent_wins
    + "<br /> Keys ";
  for (var key in this.keys) {
    this.info.innerHTML += key + " ";
  }
  this.info.innerHTML += "<br/> living: " + this.living;
  this.info.innerHTML += "<br/> states: " + Object.keys(this.player.q_states).length;
}

Game.prototype.update = function() {
  var i = document.getElementById("debug");
  this.living += 1;
  i.innerHTML = "";
  this.player.update(this);
  this.opponent.update(this);
  this.p_paddle.update(this);
  this.o_paddle.update(this);
  this.ball.update(this);
  this.player.after(this);
  this.opponent.after(this);
}

function init() {
  game = new Game();
  last_time = 0;
  animator = function() {
    var d = new Date();
    var n = d.getTime(); 
    if (n - last_time < 1000/60) {
      // skip
    } else {
      game.update();
      game.render();
    }
    animate(animator);
  };
  animator();
}


