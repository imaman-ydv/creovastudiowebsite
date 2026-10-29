import content.models


from django.db import migrations


PROJECTS = [
    ('creator-sports-network', 'Creator Sports Network', 'Strategy / Product Vision / UX/UI', '', 2025, 'Digital experiences for sports creators and their communities.', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/68667098d1fc8530da2d9ae1_CSN_Hero.avif'),
    ('entourage', 'Entourage', 'Strategy / Service design / UX/UI / Product build / Venture', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/67c1cfe0fbdf2ac2fa5f4f6d_Entourage%20v2-min.webp'),
    ('liv-x', 'LIV X', 'Strategy / Service design / UX/UI / Product build', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/6838c4cfd927f0679645c27b_livx_hero.avif'),
    ('parity-employee-nft', 'Parity Community NFT', 'Strategy / Creative Direction / NFT Design / Gamification & Rewards', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/67d437675c6d28b21d614fb1_Cyphr%20Parity%20NFT%20Hero.avif'),
    ('parity', 'Parity', 'Brand Strategy / UX/UI / Design & Development / Research', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/67d44f8e9cc71b849bd30eb7_Parity%20hero%203.avif'),
    ('spotify', 'Spotify', 'Strategy', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/673dce78c2f55ca760eef753_case-spotify-dark.webp'),
    ('tex-ai-mixologist', 'Tex — AI Mixologist', 'Strategy / Experience Design / AI Innovation / Product build', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/689222213b775bc909b38a1c_tex_hero.avif'),
    ('weber-ranch-vodka', 'Weber Ranch Vodka', 'UX/UI Design / Membership strategy / Build & launch', '', 2025, '', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/6790f4483ef9bd1a281b4407_Process_Born%20in%20Jalisco%20component%20(1)%201.avif'),
    ('krishadha', 'Krishadha', 'Brand experience', '', 2025, 'Where Royalty Finds Its Attire.', '/images/Poster5.avif'),
    ('egmmart', 'EGM MART', 'Digital platform', '', 2025, 'Engagement strategy that rewards fandom', '/images/Poster17.avif'),
    ('menmi', 'MENMI', 'Brand experience', '', 2025, 'Beginning of legacy.', '/images/Poster18.avif'),
]

INSIGHTS = [
    ('from-broadcast-to-play-cast', 'From Broadcast to Play-cast: How Gamified Live Streams Are Re-writing Sport and Why Rights-Holders Must Act Now', 'On 5 May, EA SPORTS FC Mobile quietly made history: the LA Galaxy v New York Red Bulls match was not shown on linear TV first, but inside a video-game app.', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/682dc1d100a251e2f07ceab0_ezgif-7-e065336bb0.jpg'),
    ('game-on-how-sports-fans-are-calling-the-shots', 'Game On: How Sports Fans Are Calling the Shots', "Sports viewing is in the middle of a full-blown revolution. The cozy ritual of gathering around a single TV for the big game? That's disappearing faster than last season's jersey.", 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/682c7217f8ca73465c4eceec_chris-chow-4cV0OPzIywM-unsplash.jpg'),
    ('passion-to-participation-gamified-loyalty-in-sports', 'Passion to Participation: Gamified Loyalty in Sports', 'Retailers have spent the last five years reinventing customer loyalty. Points-for-pounds schemes are being replaced by gamified experiences.', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/682b47a2a07ee9109471ffdd_pexels-brunocortes1969-32031189.webp'),
    ('the-fervency-code', 'The Fervency Code', "The power of fandom is undeniable, and it's far more complex than just cheering from the sidelines or doomscrolling through reactions.", 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/6838b8e5ae9fa72174ace2fe_fervency_code.avif'),
    ('the-secret-sauce-why-some-digital-fan-experiences-become-cultural-touchstones', 'The Secret Sauce: Why Some Digital Fan Experiences Become Cultural Touchstones', 'The digital landscape is filled with well-intentioned but ultimately forgettable fan experiences. What separates the ones people care about from those that fail to resonate?', 'https://cdn.prod.website-files.com/67312bae0d1e3af75622880b/682c989ceb1d04933083047e_geronimo-giqueaux-8ccfkXVis1Y-unsplash.webp'),
]


def seed_content(apps, schema_editor):
    SitePage = apps.get_model('content', 'SitePage')
    PageSection = apps.get_model('content', 'PageSection')
    Project = apps.get_model('content', 'Project')
    Insight = apps.get_model('content', 'Insight')

    about, _ = SitePage.objects.get_or_create(
        slug='about', defaults={'title': 'About', 'published': True, 'sort_order': 10}
    )
    sections = [
        ('about-hero-image', '', '', 'https://cdn.prod.website-files.com/672b55ccbf7fbd0d806c8f7c/679513d3ddde9f4bb03d6b0e_About%20Hero.avif'),
        ('about-heading', 'Crafting the Unforgettable', '', ''),
        ('about-tagline', 'Your story, our creativity — together, we make it unforgettable', '', ''),
        ('about-intro', '', 'At Creova Studio, we go beyond traditional web development. We craft immersive digital experiences by merging sleek, high-performance websites with breathtaking 3D visuals and cinematic VFX. Every project is designed to not just look stunning but to feel alive — engaging users, telling stories, and creating worlds they can truly step into. Whether it’s an interactive e-commerce platform, a 3D product showcase, or a visual brand experience, our goal is simple: turn imagination into reality and make your brand unforgettable.', ''),
        ('about-since', '[ Crafting since 2024 ]', '', ''),
        ('about-studio-image', '', '', '/svg/1.png'),
        ('about-studio-banner', '', '', '/images/Poster2.avif'),
        ('about-approach', '', 'Our approach is built on a foundation of creativity, strategy, and innovation. With a deep understanding of culture, design, and technology, we craft experiences that go beyond aesthetics and deliver real impact. We combine artistic vision with strategic thinking to design work that resonates, engages, and endures. By staying curious, experimenting boldly, and collaborating closely, we create solutions that not only reflect who our clients are but also shape how their audiences connect with them.', ''),
        ('about-principle-1-title', 'Listen First, Create Later', '', ''),
        ('about-principle-1-body', '', 'We believe every idea starts with a story. Our first step is always to understand you—your vision, your audience, and your purpose. By listening closely, we ensure that what we create is not just beautiful, but deeply connected to who you are.', ''),
        ('about-principle-2-title', 'Design with Meaning', '', ''),
        ('about-principle-2-body', '', 'At Creova Studio, creativity is never random. Every color, shape, and detail carries intent. Our approach blends artistry with strategy, ensuring that the work is not only visually striking but also purposeful and impactful.', ''),
        ('about-principle-3-title', 'Innovation Beyond Boundaries', '', ''),
        ('about-principle-3-body', '', 'We push beyond trends and comfort zones to craft designs that feel fresh, bold, and timeless. Experimentation fuels our process, allowing us to deliver unique experiences that stand apart in a world full of sameness.', ''),
        ('about-echo-banner', '', '', '/images/Poster3.avif'),
        ('about-help-heading', '[ How we can help ]', '', ''),
        ('about-help-intro', '', 'Solutions to problems come in different shapes and sizes. We don’t work one way; rather, we adapt to what’s needed. From creating original IP and shaping GTM strategy to designing new products, building marketing moments, and launching strategic ventures, it’s all about building with cultural and commercial intent.', ''),
        ('about-service-1-title', 'Brand Identity & Strategy', '', ''),
        ('about-service-1-body', '', 'We start by defining who you are. From naming and logo design to positioning and brand voice, we craft an identity that reflects your vision and resonates with your audience. Every brand needs a strong foundation, and we make sure yours stands out with clarity and purpose.', ''),
        ('about-service-2-title', 'Digital Presence & Experiences', '', ''),
        ('about-service-2-body', '', 'Your brand deserves to live where your audience is—online. We design and build websites, apps, and digital experiences that are not only visually striking but also seamless, functional, and engaging.', ''),
        ('about-service-3-title', 'Content Creation & Storytelling', '', ''),
        ('about-service-3-body', '', 'A brand is more than visuals—it’s the stories it tells. From high-quality photography and cinematic videos to creative campaigns and social media themes, we create content that sparks conversations and builds lasting connections with your audience.', ''),
        ('about-service-4-title', 'Growth & Market Activation', '', ''),
        ('about-service-4-body', '', 'Once the foundation is set, we help you scale. Whether it’s shaping go-to-market strategies, designing launch campaigns, or creating cultural moments, we ensure your brand grows with both commercial impact and cultural relevance—taking you from zero to 100.', ''),
        ('about-quote', '“We design with purpose—setting new standards for creativity, building meaningful connections, and driving measurable impact for brands and their audiences.”', '', ''),
    ]
    for order, (key, heading, body, image_url) in enumerate(sections):
        PageSection.objects.get_or_create(
            page=about, content_key=key,
            defaults={
                'section_type': 'image' if image_url else 'text', 'heading': heading,
                'body': body, 'image_url': image_url, 'published': True, 'sort_order': order,
            },
        )

    for order, (slug, title, category, client, year, summary, image_url) in enumerate(PROJECTS):
        Project.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title, 'category': category, 'client': client, 'year': year,
                'summary': summary, 'cover_image_url': image_url, 'published': True,
                'featured': slug in {'krishadha', 'egmmart', 'menmi'}, 'sort_order': order,
            },
        )

    for order, (slug, title, excerpt, image_url) in enumerate(INSIGHTS):
        Insight.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title, 'excerpt': excerpt, 'cover_image_url': image_url,
                'published': True, 'sort_order': order,
            },
        )



class Migration(migrations.Migration):
    dependencies = [('content', '0012_expand_insight_slug')]
    operations = [migrations.RunPython(seed_content, migrations.RunPython.noop)]
