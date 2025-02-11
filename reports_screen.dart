import 'package:flutter/material.dart';

class ReportsScreen extends StatelessWidget {
  const ReportsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Crypto Reports')),
      body: const Center(
        child: Text(
          'Here are the Crypto Reports.',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
