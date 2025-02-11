import 'package:flutter/material.dart';

class PredictionsScreen extends StatelessWidget {
  const PredictionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Crypto Predictions')),
      body: const Center(
        child: Text(
          'Here are the Crypto Predictions.',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
