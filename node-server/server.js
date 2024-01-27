const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

// Initialize express app
const app = express();

// Create HTTP server and integrate with Socket.IO
const server = http.createServer(app);
const io = socketIO(server);

// Handle socket connection
io.on('connection', socket => {
  console.log('User connected:', socket.id);

  // Join specific room
  socket.on('joinRoom', ({ roomId }) => {
    socket.join(roomId);
    console.log(`User ${socket.id} joined room: ${roomId}`);
  });

  // Relay signaling data between users in the same room
  socket.on('signal', (data) => {
    socket.to(data.roomId).emit('signal', data);
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

// Set the port the server will listen on
const PORT = process.env.PORT || 3000;

// Start the server
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
