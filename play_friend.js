var bigBoard = [[0,0,0],[0,0,0],[0,0,0]];
var smallBoard = [[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]]
var currentPlayer = -1;
var currentPlayerText = document.getElementById("current_player");
var currentBoard = [null, null];
var winner = 0;


function posClicked(btn, markerPos) {
	if (isPosValid(markerPos) && winner == 0) {
		placeMarker(btn, markerPos, currentPlayer);
		currentPlayer *= -1;
	}
}

function placeMarker(btn, markerPos, markerType) {
	//setting variables
	smallBoard[markerPos[0]][markerPos[1]][markerPos[2]][markerPos[3]] = markerType;
	bigBoard[markerPos[0]][markerPos[1]] = isBoardWon(smallBoard[markerPos[0]][markerPos[1]]);
	winner = isBoardWon(bigBoard);
	if (bigBoard[markerPos[2]][markerPos[3]] == 0) {
		currentBoard = [markerPos[2], markerPos[3]];
	} else {
		currentBoard = [null, null];
	}
	//outputting to website
	drawMarker(btn, markerPos, markerType);
}

function drawMarker(btn, markerPos, markerType) {
	let upperTable = btn.parentElement.parentElement.parentElement;
	upperTable.id = "big_table"; //remove highlighting
	if (currentBoard[0] != null && winner == 0) {
		upperTable.parentElement.parentElement.parentElement.parentElement.children[currentBoard[0]].children[currentBoard[1]].children[0].children[0].id = "big_table_selected";
	}
	if (markerType == 1) {
		btn.firstChild.src = "markers/circle.png";
		currentPlayerText.innerHTML = "cross";
		currentPlayerText.style = "color: blue;";
	} else if (markerType == -1) {
		btn.firstChild.src = "markers/cross.png";
		currentPlayerText.innerHTML = "circle";
		currentPlayerText.style = "color: red;";
	}
	if (bigBoard[markerPos[0]][markerPos[1]] == 1) {
		upperTable.id = "big_table_circle";
	} else if (bigBoard[markerPos[0]][markerPos[1]] == -1) {
		upperTable.id = "big_table_cross";
	}
	if (winner != 0) {
		won()
	}
}

function isPosValid(markerPos) {
	if (bigBoard[markerPos[0]][markerPos[1]] == 0 && smallBoard[markerPos[0]][markerPos[1]][markerPos[2]][markerPos[3]] == 0) {
		if (currentBoard[0] == null) {
			return true;
		} else if (currentBoard[0] == markerPos[0] && currentBoard[1] == markerPos[1]) {
			return true;
		}
	}
	return false;
}

function isBoardWon(board) {
	let sumList = [board[0][0]+board[1][1]+board[2][2], board[2][0]+board[1][1]+board[0][2]];
	sumList.push.apply(sumList, board.map(r => r.reduce((a, b) => a + b)));
	sumList.push.apply(sumList, board.reduce((a, b) => a.map((x, i) => x + b[i])));
	if (sumList.includes(-3)) {
		// cross won board
		return -1;
	} else if (sumList.includes(3)) {
		// circle won board
		return 1;
	}
	if ( board.reduce(function(a,b) { return a.concat(b) }).includes(0) ) {
		return 0;
	}
	return null;
}

function won() {
	if (winner == 1) {
		currentPlayerText.innerHTML = "CIRCLE WON!";
		currentPlayerText.style = "color: red;";
	} else if (winner == -1) {
		currentPlayerText.innerHTML = "CROSS WON!";
		currentPlayerText.style = "color: blue;";
	} else if (winner == null) {
		currentPlayerText.innerHTML = "TIE!";
		currentPlayerText.style = "color: white;";
	}
}

function reset() {
	bigBoard = [[0,0,0],[0,0,0],[0,0,0]];
	smallBoard = [[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]],[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]]
	currentPlayer = 1;
	currentBoard = [null, null];
	winner = 0;
	let markerBtns = document.getElementsByClassName("marker_btn")
	for (let i = 0; i < markerBtns.length; i++) {
		markerBtns[i].firstChild.src = "markers/blank.png"
	}
	let markerTables = document.getElementsByClassName("big_board")
	console.log(markerTables)
	for (let i = 0; i < markerTables.length; i++) {
		markerTables[i].children[0].id = "big_table"
	}
	currentPlayerText.innerHTML = "cross";
	currentPlayerText.style = "color: blue;";
}