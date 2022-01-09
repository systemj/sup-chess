$( document ).ready(function() {
  //
  // this is most of https://chessboardjs.com/examples/5001
  //

  // initialize empty board
  var board = Chessboard('myBoard')

  // standard chessboardjs board config
  var config = {
    draggable: true,
    position: 'start',
    orientation: 'white',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
  }

  // initialize new game
  var game = new Chess()

  // set random gameid
  $("#gameid").val(Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5));

  // initilize websocket connection
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  console.log("ready!");

  //
  // socketio event emit functions
  //

  // send current board state (on new client join)
  function sendStatus () {
    socket.emit("status",
    {
        "board_state": game.fen(),
    });
  }

  // send our move (or the initial board state)
  function sendPlayerMove (source, target) {
    socket.emit("player_move",
      {
          "board_state": game.fen(),
          "time_limit": 1,
          "opponent": $("#opponent").val(),
          "from": source,
          "to": target
      }
    );
  }

  //
  // socketio event handlers
  //

  // handle connect event
  socket.on('connect', function() {
    console.log("connected");
  });

  // remote move event
  socket.on('remote_move', function(data) {
    console.log("remote_move");
    console.log(data);
    if ($("#role").val() === "observer") {
      board.position(data.board_state)
    } else {
      valid = game.move({from: data.from, to: data.to});
      if (valid != null) {
        board.position(game.fen());
      }
    }
  });

  // set status
  socket.on('status', function(data) {
    if ($("#role").val() != "w") {
      board.position(data.board_state);
      game = new Chess(data.board_state);
    }
  });

  // client join event
  socket.on('joined_game', function(data) {
    console.log(data);
    if ($("#role").val() === "w") {
      sendStatus();
    }
  });

  //
  // chessboardjs event handlers
  //

  // player piece movement
  function onDragStart (source, piece, position, orientation) {
    // observers can't move pieces
    if ($("#role").val() === "observer") return false;

    // do not pick up pieces if the game is over
    if (game.game_over()) return false;

    // do not pick up the other player's pieces
    if (($("#role").val() === 'w' && piece.search(/^b/) !== -1) ||
        ($("#role").val() === 'b' && piece.search(/^w/) !== -1)) {
        return false
    }
    // or if it's not that side's turn
    if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false
    }
  }

  function onDrop (source, target) {
    // see if the move is legal
    var move = game.move({
      from: source,
      to: target,
      promotion: 'q' // NOTE: always promote to a queen for example simplicity
    })

    // illegal move
    if (move === null) return 'snapback'

    // send our move
    sendPlayerMove(source, target);
  }

  // update the board position after the piece snap
  // for castling, en passant, pawn promotion
  function onSnapEnd () {
    board.position(game.fen())
  }

  //
  // button click handlers
  //

  // flip board orientation
  $("#flip").on("click", function() {
    board.flip();
  });

  // Start, join, or observe a game
  $("#start").on("click", function() {
    // disable the settings buttons
    $("#gameid").prop("disabled",true);
    $("#role").prop("disabled",true);
    $("#opponent").prop("disabled",true);
    $("#start").prop("disabled",true);

    // join the game
    socket.emit("join_game", { "gameid": $("#gameid").val()})

    // if the role is player2
    if ($("#role").val() === "b") {
      // flip the board orientation to black
      config.orientation = "black";

      // if the opponent is a chess engine, send the initial board state to start the game
      if ($("#opponent").val() != "human") {
        sendPlayerMove("", "");
      }
    }

    // update the board to the starting position
    board = Chessboard('myBoard', config);
  });

});