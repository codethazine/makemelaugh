const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
    cors: {
      origin: "*", // Allow all origins or specify the ones you want to allow
      methods: ["GET", "POST"], // Allow specific HTTP methods
      allowedHeaders: ["my-custom-header"], // Allow specific headers
      credentials: true // Allow credentials
    }
});

// Store room data
let roomCount = 0;
const roomParticipants = {};

io.on('connection', socket => {
  console.log('User connected:', socket.id);

  socket.on('joinNextAvailableRoom', () => {
    let roomId = roomCount.toString();
    if (!roomParticipants[roomId] || roomParticipants[roomId].length < 2) {
      roomParticipants[roomId] = roomParticipants[roomId] || [];
      roomParticipants[roomId].push(socket.id);
      socket.join(roomId);
      console.log(`User ${socket.id} joined room: ${roomId}`);
    } else {
      roomId = (++roomCount).toString();
      roomParticipants[roomId] = [socket.id];
      socket.join(roomId);
      console.log(`User ${socket.id} joined new room: ${roomId}`);
    }
    socket.emit('joinedRoom', roomId);
  });

  // Relay signaling data between users in the same room
  socket.on('signal', (data) => {
    socket.to(data.roomId).emit('signal', data);
  });

  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
    // Remove the user from the room
    for (const roomId in roomParticipants) {
      const index = roomParticipants[roomId].indexOf(socket.id);
      if (index !== -1) {
        roomParticipants[roomId].splice(index, 1);
        break;
      }
    }
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
