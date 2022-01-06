$( document ).ready(function() {
    //
    // this is most of https://chessboardjs.com/examples/5001
    //
    var board = null
    var game = new Chess()

    // empty board
    var board = Chessboard('myBoard')

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
    
    function onDrop (source, target) {
      // see if the move is legal
      var move = game.move({
        from: source,
        to: target,
        promotion: 'q' // NOTE: always promote to a queen for example simplicity
      })
    
      // illegal move
      if (move === null) return 'snapback'
    
      // log some info about the move
      player_move_info = {
        board_state: game.fen(),
        player: $("#role").val(),
        from: source,
        to: target
      }
      console.log(player_move_info)

      // send our move
      sendPlayerMove(source, target);
    }
    
    // update the board position after the piece snap
    // for castling, en passant, pawn promotion
    function onSnapEnd () {
      board.position(game.fen())
    }
    
    var config = {
      draggable: true,
      position: 'start',
      orientation: 'white',
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd
    }

    // Start, join, or observe a game
    $("#start").on("click", function() {
      // disable the settings buttons
      $("#gameid").prop("disabled",true);
      $("#role").prop("disabled",true);
      $("#opponent").prop("disabled",true);
      $("#start").prop("disabled",true);
      $("#resign").prop("disabled",false);

      // // if the role is player1
      // if ($("#role").val() === "w") {
      //   // generate gameid
      //   var x = gameid;
      // }

      // join the game
      socket.emit("join_game", { "gameid": $("#gameid").val()})

      // if the role is player2
      if ($("#role").val() === "b") {
        // flip the board orientation to black
        config.orientation = "black";

        // if the opponent is a chess engine, send the initial board state to start the game
        //if ($("#opponent").val() != "human") {
          sendPlayerMove("", "");
        //}
      }
      
      // update the board to the starting position
      board = Chessboard('myBoard', config);
    });

    // connect to the backend
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // handle connect event
    socket.on('connect', function() {
        // socket.emit('joined', {});
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

    socket.on('*', function(data) { console.log(data)});

    // joined game event
    socket.on('joined_game', function(data) {
      console.log(data);
    });

     // socket.disconnect();

    console.log( "ready!" );
});