import React, { useState } from 'react';

function Controls({ onGenerateMaze, onSolveMaze }) {
    // Estados para armazenar as entradas do usuário
    const [largura, setLargura] = useState('');
    const [altura, setAltura] = useState('');
    const [paredes, setParedes] = useState('');
    const [algorithm, setAlgorithm] = useState('bfs'); // Padrão para BFS

    // Função de clique para gerar o labirinto com as informações do usuário
    const handleGenerateMazeClick = () => {
        onGenerateMaze({
            largura: parseInt(largura),
            altura: parseInt(altura),
            paredes: parseInt(paredes)
        });
    };

    // Função de clique para resolver o labirinto com o algoritmo selecionado
    const handleSolveMazeClick = () => {
        onSolveMaze(algorithm);
    };

    return (
        <div>
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
                    placeholder="Número de paredes para remover"
                />
            </label>
            <button onClick={handleGenerateMazeClick}>Gerar Labirinto</button>

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
    );
}

export default Controls;
