import 'package:flutter/material.dart';

import 'pages/content_pages.dart';

const _paper = Color(0xFFECECE9);
const _ink = Color(0xFF050505);

void main() {
  runApp(const CreovaApp());
}

class CreovaApp extends StatelessWidget {
  const CreovaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Creova Studio',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: _paper,
        colorScheme: ColorScheme.fromSeed(seedColor: _ink, surface: _paper),
        fontFamily: 'Bandit Condensed',
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final width = constraints.maxWidth;
            final compact = width < 600;
            final pageInset = compact ? 13.0 : 24.0;
            final titleSize = (width * (compact ? 0.085 : 0.095))
                .clamp(32.0, 170.0)
                .toDouble();

            return Padding(
              padding: EdgeInsets.fromLTRB(pageInset, 8, pageInset, 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  SizedBox(
                    height: compact ? 34 : 44,
                    child: Align(
                      alignment: Alignment.centerRight,
                      child: TextButton(
                        onPressed: () => _showMenu(context),
                        style: TextButton.styleFrom(
                          foregroundColor: _ink,
                          padding: EdgeInsets.zero,
                          minimumSize: const Size(48, 34),
                          tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                        ),
                        child: Text(
                          'MENU',
                          style: TextStyle(
                            fontFamily: 'Bandit Condensed',
                            fontSize: compact ? 15 : 18,
                            height: 1,
                          ),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: compact ? 12 : 18),
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(compact ? 6 : 12),
                      child: Stack(
                        fit: StackFit.expand,
                        children: [
                          const ColoredBox(color: _ink),
                          Image.asset(
                            'assets/images/Logo.png',
                            fit: BoxFit.contain,
                            errorBuilder: (context, error, stackTrace) => const SizedBox(),
                          ),
                          IgnorePointer(
                            child: LayoutBuilder(
                              builder: (context, visualConstraints) {
                                final lines = visualConstraints.maxWidth < 600 ? 4 : 10;
                                return Stack(
                                  children: [
                                    for (var index = 1; index <= lines; index++)
                                      Positioned(
                                        left: visualConstraints.maxWidth * index / (lines + 1) - 1.5,
                                        top: 0,
                                        bottom: 0,
                                        child: const SizedBox(
                                          width: 3,
                                          child: ColoredBox(color: _paper),
                                        ),
                                      ),
                                  ],
                                );
                              },
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  SizedBox(height: compact ? 12 : 18),
                  Text(
                    compact ? 'Turning Imagination\nInto Reality' : 'Turning Imagination Into Reality',
                    maxLines: compact ? 2 : 1,
                    softWrap: compact,
                    overflow: TextOverflow.clip,
                    style: TextStyle(
                      color: _ink,
                      fontFamily: 'Bandit Condensed',
                      fontSize: titleSize,
                      height: compact ? 0.9 : 0.88,
                      letterSpacing: compact ? -0.5 : -2.5,
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  void _showMenu(BuildContext context) {
    final homeContext = context;
    showModalBottomSheet<void>(
      context: context,
      backgroundColor: _ink,
      showDragHandle: false,
      builder: (sheetContext) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(24, 32, 24, 36),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              for (final item in [
                ('Work', const ProjectsPage()),
                ('Insights', const InsightsPage()),
                ('About', const AboutPage()),
                ('VMV', const ValuesPage()),
                ('Contact', const ContactPage()),
              ])
                Semantics(
                  button: true,
                  child: InkWell(
                    onTap: () {
                      Navigator.of(sheetContext).pop();
                      Navigator.of(homeContext).push(MaterialPageRoute<void>(builder: (_) => item.$2));
                    },
                    child: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      child: Text(
                        item.$1,
                        style: const TextStyle(
                          color: _paper,
                          fontFamily: 'Bandit Condensed',
                          fontSize: 42,
                          height: 1,
                        ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
