import React, { useState } from 'react';

function Controls({ onGenerateMaze, onSolveMaze }) {
    const [largura, setLargura] = useState('');
    const [altura, setAltura] = useState('');
    const [paredes, setParedes] = useState('');
    const [algorithm, setAlgorithm] = useState('bfs'); // Padrão para BFS

    const handleGenerateMazeClick = () => {
        onGenerateMaze({
            largura: parseInt(largura),
            altura: parseInt(altura),
            paredes: parseInt(paredes)
        });
    };

    const handleSolveMazeClick = () => {
        onSolveMaze(algorithm);
    };

    return (
        <div className="controls-wrapper">
            <div className="controls-container">
                <h3>Gerar Labirinto</h3>
                <label>
                    Largura:
                    <input
                        type="number"
                        value={largura}
                        onChange={(e) => setLargura(e.target.value)}
                        placeholder="Digite a largura"
                    />
                </label>
                <label>
                    Altura:
                    <input
                        type="number"
                        value={altura}
                        onChange={(e) => setAltura(e.target.value)}
                        placeholder="Digite a altura"
                    />
                </label>
                <label>
                    Paredes:
                    <input
                        type="number"
                        value={paredes}
                        onChange={(e) => setParedes(e.target.value)}
                        placeholder="Remover paredes"
                    />
                </label>
                <button onClick={handleGenerateMazeClick}>Gerar Labirinto</button>
            </div>

            <div className="controls-container">
                <h3>Solucionar Labirinto</h3>
                <label>
                    Algoritmo:
                    <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
                        <option value="bfs">BFS</option>
                        <option value="dfs">DFS</option>
                    </select>
                </label>
                <button onClick={handleSolveMazeClick}>Solucionar Labirinto</button>
            </div>
        </div>
    );
}

export default Controls;
