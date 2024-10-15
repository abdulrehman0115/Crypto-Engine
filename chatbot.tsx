import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, FlatList, Text, StyleSheet } from 'react-native';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
}

const ConversationTab: React.FC = () => {
  const [inputMessage, setInputMessage] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      // Add user message
      const newMessage: Message = {
        id: Math.random().toString(), // Unique ID for each message
        text: inputMessage,
        isUser: true,
      };

      // Add computer response
      const responseMessage: Message = {
        id: Math.random().toString(),
        text: "This is a sample output from the computer.", // Sample response
        isUser: false,
      };

      // Update messages state
      setMessages((prevMessages) => [...prevMessages, newMessage, responseMessage]);
      setInputMessage(''); // Clear input field
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <View style={[styles.messageContainer, item.isUser ? styles.userMessage : styles.computerMessage]}>
            <Text style={[styles.messageText, item.isUser ? styles.userText : styles.computerText]}>
              {item.text}
            </Text>
          </View>
        )}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.messageList}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Message CryptoBot"
          value={inputMessage}
          onChangeText={setInputMessage}
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSendMessage}>
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  messageList: {
    paddingBottom: 16,
  },
  messageContainer: {
    padding: 10,
    borderRadius: 20, // Adjusted for oval shape
    marginVertical: 5,
    maxWidth: '80%',
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#007bff', // User message color
  },
  computerMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#333', // Darker color for computer messages
  },
  messageText: {
    fontSize: 16,
  },
  userText: {
    color: '#fff', // White text for user messages
  },
  computerText: {
    color: '#fff', // White text for computer messages
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  input: {
    flex: 1,
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 20, // Adjusted for oval shape
    paddingHorizontal: 10,
    marginRight: 10, // Space between input and button
  },
  sendButton: {
    backgroundColor: '#007bff',
    borderRadius: 20, // Adjusted for oval shape
    paddingVertical: 10,
    paddingHorizontal: 20, // Increased horizontal padding for a more oval look
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

export default ConversationTab;
