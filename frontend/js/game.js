
function onChange (oldPos, newPos) {
    console.log('Position changed:');
    console.log('Old position: ' + Chessboard.objToFen(oldPos));
    console.log('New position: ' + Chessboard.objToFen(newPos));
    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    socket.emit("player_move", {"board_state": Chessboard.objToFen(newPos)});
}


$( document ).ready(function() {

    //
    // this is most of https://chessboardjs.com/examples/5001
    //
    var board = null
    var game = new Chess()
    
    function onDragStart (source, piece, position, orientation) {
      // do not pick up pieces if the game is over
      if (game.game_over()) return false
    
      // only pick up pieces for White
      if (piece.search(/^b/) !== -1) return false
    }
    
    function makeRandomMove () {
      console.log(game.fen());
      socket.emit("player_move",
        {
            "board_state": game.fen(),
            "time_limit": 1,
            "engine": "gnuchess"
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
    
      // make random legal move for black
      makeRandomMove();
    }
    
    // update the board position after the piece snap
    // for castling, en passant, pawn promotion
    function onSnapEnd () {
      board.position(game.fen())
    }
    
    var config = {
      draggable: true,
      position: 'start',
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd
    }
    board = Chessboard('myBoard', config)

    // testing...
    socket = io.connect('http://127.0.0.1:8000');
    // socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    socket.on('connect', function() {
        // socket.emit('joined', {});
        console.log("connected");
    });

    socket.on('remote_move', function(data) {
        console.log(data);
        lol = game.move({from: data.from, to: data.to});
        console.log(lol);
        board.position(game.fen());
        //board.position(data.board)
    });

    // socket.disconnect();

    console.log( "ready!" );
});