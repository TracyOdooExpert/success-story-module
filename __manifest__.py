# -*- coding: utf-8 -*-
{
    'name': 'Success Stories Builder',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Manage and publish testimonials/success stories with dynamic pages and slider snippets',
    'description': """
        Success Stories Builder
        =======================
        
        This module allows you to:
        * Create and manage success stories/testimonials from the backend
        * Automatically generate individual web pages for each published story
        * Display stories in a beautiful slider snippet on any website page
        * Filter stories by category
        * SEO-optimized individual pages with clean URLs
        * Link stories to products with CTA buttons
        
        Features:
        ---------
        - Backend form with all necessary fields (client, logo, images, video, texts, etc.)
        - Automatic page generation with unique URLs
        - Draggable slider snippet for website builder
        - Responsive design (desktop/mobile)
        - Category filtering
        - Navigation arrows in slider
        - Publish/unpublish option
    """,
    'author': 'Adil Akbar',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'website',
        'contacts',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/success_story_views.xml',
        'views/menu_views.xml',
        'views/success_story_templates.xml',
        'views/success_story_snippets.xml',
        'data/website_menu_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'success_stories_builder/static/src/scss/success_stories.scss',
            'success_stories_builder/static/src/js/success_stories_slider.js',
        ],
    },
    'images': ['static/description/icon.svg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
