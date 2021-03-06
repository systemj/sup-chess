$( document ).ready(function() {
  //
  // this is most of https://chessboardjs.com/examples/5001
  //

  // standard chessboardjs board config
  var config = {
    draggable: true,
    position: '',
    orientation: 'white',
    pieceTheme: 'img/chesspieces/{piece}.svg',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare
  }

  // initialize empty board
  var board = Chessboard('myBoard', config)

  // initialize new game
  var game = new Chess()

  // valid move indicator colors
  var whiteSquareGrey = '#a9a9a9'
  var blackSquareGrey = '#696969'

  // set random gameid
  $("#gameid").val(Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5));

  // initilize websocket connection
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  console.log("ready!");

  //
  // helper functions
  //

  // remove square valid move indication
  function removeGreySquares () {
    $('#myBoard .square-55d63').css('background', '')
  }

  // set square valid move move indication
  function greySquare (square) {
    var $square = $('#myBoard .square-' + square)

    var background = whiteSquareGrey
    if ($square.hasClass('black-3c85d')) {
      background = blackSquareGrey
    }

    $square.css('background', background)
  }

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
  socket.on('player_move', function(data) {
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
  socket.on('join_game', function(data) {
    console.log(data);
    if ($("#role").val() === "w") {
      sendStatus();
    }
    if (($("#role").val() === "b") && ($("#opponent").val() !== "human")) {
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

  function onMouseoverSquare (square, piece) {
    if ($("#show_legal_moves").prop("checked") === false) return;

    // only show moves on the player's turn
    if (game.turn() !== $("#role").val()) return;

    // get list of possible moves for this square
    var moves = game.moves({
      square: square,
      verbose: true
    })

    // exit if there are no moves available for this square
    if (moves.length === 0) return

    // highlight the square they moused over
    greySquare(square)

    // highlight the possible squares for this piece
    for (var i = 0; i < moves.length; i++) {
      greySquare(moves[i].to)
    }
  }

  function onMouseoutSquare (square, piece) {
    removeGreySquares()
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
    config.position = 'start';
    board = Chessboard('myBoard', config);
  });

});