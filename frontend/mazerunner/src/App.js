import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Head from './components/Head';
import Footer from './components/Footer'
import Home from './components/Home';
import Controls from './components/Controls';
import Canvas from './components/Canvas';
import './App.css';
import NeonBackground from'./components/NeonBackground';
import Info from './components/infoextras'


const socket = io('http://127.0.0.1:5000');

function App() {
    const [mazeMatrix, setMazeMatrix] = useState(null);

    useEffect(() => {
        socket.on('receive_labirinto', (data) => {
            setMazeMatrix(data.image);
        });

        socket.on('receive_matrix', (data) => {
            setMazeMatrix(data.image);
        });

        socket.on('error', (data) => {
            console.error('Erro:', data.message);
        });

        return () => {
            socket.off('receive_labirinto');
            socket.off('receive_matrix');
            socket.off('error');
        };
    }, []);

    const handleGenerateMaze = ({ largura, altura, paredes }) => {
        if (largura && altura || paredes) {
            socket.emit('send_labirinto', {
                largura,
                altura,
                paredes
            });
        } else {
            alert("Por favor, preencha todos os campos para gerar o labirinto.");
        }
    };

    const handleSolveMaze = (algorithm) => {
        if (algorithm === 'bfs' || algorithm === 'dfs') {
            socket.emit('send_matrix', { algorithm });
        } else {
            alert("Algoritmo inválido. Escolha 'bfs' ou 'dfs'.");
        }
    };

    return (
        <div className="App">
            <NeonBackground />
            <div className='conteudo'> 
                <Head />
                <Home></Home>
                <h1 style={{ color: '#f39c12', marginTop:'100px' }}>Selecione as configurações do seu labirinto e a solução</h1>
                <Controls onGenerateMaze={handleGenerateMaze} onSolveMaze={handleSolveMaze} />
                <h1 style={{ color: '#f39c12' }}>Labirinto</h1>
                <Canvas matrix={mazeMatrix} />
                <Info />

            </div>
            <Footer />
        </div>
    );
}

export default App;
