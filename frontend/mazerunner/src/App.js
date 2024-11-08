import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Head from './components/Head';
import Footer from './components/Footer'
import Home from './components/Home';
import Controls from './components/Controls';
import Canvas from './components/Canvas';
import './App.css';


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

  const handleGenerateMaze = () => {
    const largura = prompt("Digite a largura do labirinto:");
    const altura = prompt("Digite a altura do labirinto:");
    const paredes = prompt("Digite o número de paredes para remover:");

    if (largura && altura && paredes) {
      socket.emit('send_labirinto', {
        largura: parseInt(largura),
        altura: parseInt(altura),
        paredes: parseInt(paredes)
      });
    }
  };

  const handleSolveMaze = () => {
    const algorithm = prompt("Digite o algoritmo (bfs ou dfs):");

    if (algorithm === 'bfs' || algorithm === 'dfs') {
      socket.emit('send_matrix', { algorithm: algorithm });
    } else {
      alert("Algoritmo inválido. Escolha 'bfs' ou 'dfs'.");
    }
  };
  

  return (
    <div className="App">
      <Head/>
      <Home></Home>
      <div></div>
      <Controls onGenerateMaze={handleGenerateMaze} onSolveMaze={handleSolveMaze} />
      <h2>Labirinto</h2>
      <Canvas matrix={mazeMatrix} />
      <Footer/>
    </div>
  );
}

export default App;
