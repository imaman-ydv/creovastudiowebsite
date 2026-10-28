import 'package:flutter/material.dart';

import '../data/site_api.dart';

const _paper = Color(0xFFECECE9);
const _ink = Color(0xFF050505);

class ContentScaffold extends StatelessWidget {
  const ContentScaffold({
    required this.title,
    required this.child,
    super.key,
  });

  final String title;
  final Widget child;

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: _paper,
        appBar: AppBar(
          backgroundColor: _paper,
          foregroundColor: _ink,
          title: Text(title.toUpperCase(), style: const TextStyle(fontFamily: 'Bandit Condensed')),
        ),
        body: child,
      );
}

class ProjectsPage extends StatefulWidget {
  const ProjectsPage({super.key});

  @override
  State<ProjectsPage> createState() => _ProjectsPageState();
}

class _ProjectsPageState extends State<ProjectsPage> {
  final _api = SiteApi();
  late Future<List<ProjectSummary>> _projects;

  @override
  void initState() {
    super.initState();
    _projects = _api.fetchProjects();
  }

  @override
  Widget build(BuildContext context) => ContentScaffold(
        title: 'Work',
        child: FutureBuilder<List<ProjectSummary>>(
          future: _projects,
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const Center(child: CircularProgressIndicator(color: _ink));
            }
            if (snapshot.hasError) {
              return _StatusMessage(
                message: 'Projects are not available right now.',
                action: () => setState(() => _projects = _api.fetchProjects()),
              );
            }
            final projects = snapshot.data ?? const <ProjectSummary>[];
            if (projects.isEmpty) {
              return const _EmptyMessage(
                title: 'New work is on the way.',
                detail: 'Published projects added in the studio admin will appear here.',
              );
            }
            return LayoutBuilder(
              builder: (context, constraints) {
                final columns = constraints.maxWidth >= 1000
                    ? 3
                    : constraints.maxWidth >= 620
                        ? 2
                        : 1;
                return GridView.builder(
                  padding: const EdgeInsets.fromLTRB(18, 12, 18, 32),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: columns,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 26,
                    childAspectRatio: columns == 1 ? 0.78 : 0.78,
                  ),
                  itemCount: projects.length,
                  itemBuilder: (context, index) => _ProjectCard(project: projects[index]),
                );
              },
            );
          },
        ),
      );
}

class _ProjectCard extends StatelessWidget {
  const _ProjectCard({required this.project});

  final ProjectSummary project;

  @override
  Widget build(BuildContext context) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: ColoredBox(
                color: _ink,
                child: project.coverImageUrl.isEmpty
                    ? const Center(child: Icon(Icons.auto_awesome, color: _paper, size: 36))
                    : Image.network(
                        project.coverImageUrl,
                        width: double.infinity,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) => const Center(
                          child: Icon(Icons.image_not_supported_outlined, color: _paper, size: 32),
                        ),
                      ),
              ),
            ),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: Text(
                  project.title,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(fontFamily: 'Bandit Condensed', fontSize: 28, height: 1),
                ),
              ),
              if (project.year != null) Text(project.year.toString()),
            ],
          ),
          if (project.category.isNotEmpty) ...[
            const SizedBox(height: 5),
            Text(project.category.toUpperCase(), style: const TextStyle(fontSize: 11, letterSpacing: 1.1)),
          ],
          if (project.summary.isNotEmpty) ...[
            const SizedBox(height: 7),
            Text(project.summary, maxLines: 3, overflow: TextOverflow.ellipsis),
          ],
        ],
      );
}

class InsightsPage extends StatefulWidget {
  const InsightsPage({super.key});

  @override
  State<InsightsPage> createState() => _InsightsPageState();
}

class _InsightsPageState extends State<InsightsPage> {
  final _api = SiteApi();
  late Future<List<InsightSummary>> _insights;

  @override
  void initState() {
    super.initState();
    _insights = _api.fetchInsights();
  }

  @override
  Widget build(BuildContext context) => ContentScaffold(
        title: 'Insights',
        child: FutureBuilder<List<InsightSummary>>(
          future: _insights,
          builder: (context, snapshot) {
            if (snapshot.connectionState != ConnectionState.done) {
              return const Center(child: CircularProgressIndicator(color: _ink));
            }
            if (snapshot.hasError) {
              return _StatusMessage(
                message: 'Insights are not available right now.',
                action: () => setState(() => _insights = _api.fetchInsights()),
              );
            }
            final insights = snapshot.data ?? const <InsightSummary>[];
            if (insights.isEmpty) {
              return const _EmptyMessage(
                title: 'Fresh ideas are on the way.',
                detail: 'Published articles added in the studio admin will appear here.',
              );
            }
            return ListView.separated(
              padding: const EdgeInsets.fromLTRB(18, 12, 18, 32),
              itemCount: insights.length,
              separatorBuilder: (context, index) => const Divider(height: 32, color: _ink),
              itemBuilder: (context, index) => _InsightRow(insight: insights[index]),
            );
          },
        ),
      );
}

class _InsightRow extends StatelessWidget {
  const _InsightRow({required this.insight});

  final InsightSummary insight;

  @override
  Widget build(BuildContext context) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(insight.title, style: const TextStyle(fontFamily: 'Bandit Condensed', fontSize: 32, height: 1)),
          if (insight.publishedAt case final date?) ...[
            const SizedBox(height: 6),
            Text(date.substring(0, 10), style: const TextStyle(fontSize: 11, letterSpacing: 1.1)),
          ],
          if (insight.excerpt.isNotEmpty) ...[
            const SizedBox(height: 10),
            Text(insight.excerpt),
          ],
        ],
      );
}

class ContactPage extends StatefulWidget {
  const ContactPage({super.key});

  @override
  State<ContactPage> createState() => _ContactPageState();
}

class _ContactPageState extends State<ContactPage> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _email = TextEditingController();
  final _message = TextEditingController();
  final _api = SiteApi();
  bool _sending = false;

  @override
  void dispose() {
    _name.dispose();
    _email.dispose();
    _message.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _sending = true);
    try {
      await _api.submitContact(
        name: _name.text.trim(),
        email: _email.text.trim(),
        message: _message.text.trim(),
      );
      if (!mounted) return;
      _formKey.currentState!.reset();
      _name.clear();
      _email.clear();
      _message.clear();
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Thanks — your message has been received.')));
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error.toString())));
    } finally {
      if (mounted) setState(() => _sending = false);
    }
  }

  @override
  Widget build(BuildContext context) => ContentScaffold(
        title: 'Contact',
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 680),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Text('Let’s make something unforgettable.', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 42, height: 1)),
                    const SizedBox(height: 24),
                    _ContactField(controller: _name, label: 'Name'),
                    _ContactField(controller: _email, label: 'Email', keyboardType: TextInputType.emailAddress),
                    _ContactField(controller: _message, label: 'Message', maxLines: 6),
                    const SizedBox(height: 12),
                    FilledButton(
                      onPressed: _sending ? null : _submit,
                      style: FilledButton.styleFrom(backgroundColor: _ink, foregroundColor: _paper),
                      child: Text(_sending ? 'SENDING…' : 'SEND MESSAGE'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      );
}

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) => ContentScaffold(
        title: 'About',
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 900),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Crafting the Unforgettable', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 58, height: 0.98)),
                  const SizedBox(height: 24),
                  const Text('We craft immersive digital experiences by merging thoughtful design, high-performance websites, and cinematic visuals. Every project is shaped around a clear story and built to help a brand connect with its audience.'),
                  const SizedBox(height: 20),
                  const Text('Creative. Strategic. Curious.', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 36)),
                  const Text('We work closely with our clients, experiment boldly, and combine creative direction with technology to make ideas tangible.'),
                ],
              ),
            ),
          ),
        ),
      );
}

class ValuesPage extends StatelessWidget {
  const ValuesPage({super.key});

  @override
  Widget build(BuildContext context) => ContentScaffold(
        title: 'Vision, Mission & Values',
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 900),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Make digital feel human.', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 58, height: 0.98)),
                  const SizedBox(height: 24),
                  const Text('Vision', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 34)),
                  const Text('Build a more imaginative digital world where brands and people connect through meaningful experiences.'),
                  const SizedBox(height: 18),
                  const Text('Mission', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 34)),
                  const Text('Bring strategy, design, and technology together to create work that moves businesses forward.'),
                  const SizedBox(height: 18),
                  const Text('Values', style: TextStyle(fontFamily: 'Bandit Condensed', fontSize: 34)),
                  const Text('Curiosity, craft, collaboration, and care guide every project from first conversation to launch.'),
                ],
              ),
            ),
          ),
        ),
      );
}

class _ContactField extends StatelessWidget {
  const _ContactField({required this.controller, required this.label, this.maxLines = 1, this.keyboardType});

  final TextEditingController controller;
  final String label;
  final int maxLines;
  final TextInputType? keyboardType;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 14),
        child: TextFormField(
          controller: controller,
          maxLines: maxLines,
          keyboardType: keyboardType,
          decoration: InputDecoration(
            labelText: label,
            border: const OutlineInputBorder(),
            focusedBorder: const OutlineInputBorder(borderSide: BorderSide(color: _ink, width: 2)),
          ),
          validator: (value) => value == null || value.trim().isEmpty ? 'Please enter your $label.' : null,
        ),
      );
}

class _StatusMessage extends StatelessWidget {
  const _StatusMessage({required this.message, required this.action});

  final String message;
  final VoidCallback action;

  @override
  Widget build(BuildContext context) => Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 12),
            TextButton(onPressed: action, child: const Text('TRY AGAIN')),
          ],
        ),
      );
}

class _EmptyMessage extends StatelessWidget {
  const _EmptyMessage({required this.title, required this.detail});

  final String title;
  final String detail;

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(title, textAlign: TextAlign.center, style: const TextStyle(fontFamily: 'Bandit Condensed', fontSize: 34)),
              const SizedBox(height: 8),
              Text(detail, textAlign: TextAlign.center),
            ],
          ),
        ),
      );
}
