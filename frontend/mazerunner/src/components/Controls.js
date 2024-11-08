import React from 'react';

function Controls({ onGenerateMaze, onSolveMaze }) {
  return (
    <div>
      <button onClick={onGenerateMaze}>Gerar Labirinto</button>
      <button onClick={onSolveMaze}>Solucionar Labirinto</button>
    </div>
  );
}

export default Controls;
