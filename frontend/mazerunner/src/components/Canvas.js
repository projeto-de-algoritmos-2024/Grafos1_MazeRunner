import React, { useRef, useEffect } from 'react';

function Canvas({ matrix }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (matrix && canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const width = matrix[0].length;
      const height = matrix.length;
      const scaleFactor = 10;

      canvas.width = width * scaleFactor;
      canvas.height = height * scaleFactor;

      matrix.forEach((row, y) => {
        row.forEach((pixel, x) => {
          const color = `rgb(${pixel[0]}, ${pixel[1]}, ${pixel[2]})`;
          ctx.fillStyle = color;
          ctx.fillRect(x * scaleFactor, y * scaleFactor, scaleFactor, scaleFactor);
        });
      });
    }
  }, [matrix]);

  return <canvas id="canvas" ref={canvasRef} style={{ border: '1px solid black', display: 'block', margin: '20px auto' }} />;
}

export default Canvas;
