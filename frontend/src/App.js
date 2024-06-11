import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:5000');


function App() {
    const [messages, setMessages] = useState([]);
    const [gameId, setGameId] = useState('');
    const [board, setBoard] = useState([]);

    useEffect(() => {
        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('status', (data) => {
            setMessages((prev) => [...prev, data.msg]);
        });

        socket.on('move', (data) => {
            setBoard(data.board_state);
        });

        return () => {
            socket.off('connect');
            socket.off('status');
            socket.off('move');
        };
    }, []);

    const createGame = () => {
        fetch('/create_game', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                setGameId(data.game_id);
                socket.emit('join', { game_id: data.game_id });
            });
    };

    const joinGame = () => {
        const id = prompt('Enter Game ID:');
        const color = prompt('Enter Color (black/white):');
        fetch('/join_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game_id: id, color: color })
        }).then(() => {
            setGameId(id);
            socket.emit('join', { game_id: id });
        });
    };

    const sendMessage = (x, y, color) => {
        socket.emit('move', { game_id: gameId, move: [x, y, color] });
    };

    return (
        <div className="App">
            <button onClick={createGame}>Create Game</button>
            <button onClick={joinGame}>Join Game</button>
            <div>Game ID: {gameId}</div>
            <ul>
                {messages.map((msg, index) => (
                    <li key={index}>{msg}</li>
                ))}
            </ul>
            <div>
                {board.map((row, rowIndex) => (
                    <div key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <button key={cellIndex} onClick={() => sendMessage(rowIndex, cellIndex, 'black')}>
                                {cell}
                            </button>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;