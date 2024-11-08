import React from 'react';

function Info() {
  return (
    <div className='conteiner_info'>
        <div className='info'>
            <div className='sub'>
                <h2 className='tu'>Legenda das cores:</h2>

                <p className='line'><span className='vermelho'>Vermelho:</span> É o caminho sendo percorrido</p>
                <p className='line'><span className='amarelo'>Amarelo:</span> É a solução</p>
                <p className='line'><span className ='verde' > Verde:</span> Backtraking da DFS</p>
            </div>
        </div>
    </div>
  );
}

export default Info;
