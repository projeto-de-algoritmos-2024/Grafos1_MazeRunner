import React from 'react';

function Footer() {
  return (
    <footer>
        <div class="footer-container">
            <div class="footer-section">
                <h3>Sobre Nós</h3>
                <p>Somos alunos da UNB e o intuito desse projeto é aplicar teoria de grafos na prática</p>
            </div>
            <div class="footer-section">
                <h3>GitHub do projeto</h3>
                <div class="social-icons">
                    <a href="https://github.com/projeto-de-algoritmos-2024/Grafos1_MazeRunner" aria-label="GitHub">🌐</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2024 Projeto de Algoritmos. Todos os direitos reservados a Carlos Alves e Hugo Queiroz.
        </div>
    </footer>
  );
}

export default Footer;
