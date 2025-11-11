# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL


class SuccessStoryController(http.Controller):
    
    @http.route(['/success-story/<string:slug>'], type='http', auth='public', website=True, sitemap=True)
    def success_story_detail(self, slug, **kwargs):
        """
        Display individual success story page
        """
        # Find the success story by URL slug
        story = request.env['success.story'].sudo().search([
            ('url_slug', '=', slug),
            ('is_published', '=', True)
        ], limit=1)
        
        if not story:
            return request.render('website.404')
        
        # Get related stories from the same category
        related_stories = request.env['success.story'].sudo().search([
            ('category', '=', story.category),
            ('id', '!=', story.id),
            ('is_published', '=', True)
        ], limit=3, order='publication_date desc')
        
        values = {
            'story': story,
            'related_stories': related_stories,
            'main_object': story,
        }
        
        return request.render('success_stories_builder.success_story_detail_page', values)
    
    @http.route(['/success-stories', '/success-stories/category/<string:category>'], 
                type='http', auth='public', website=True, sitemap=True)
    def success_stories_list(self, category=None, **kwargs):
        """
        Display list of all success stories with optional category filter
        """
        domain = [('is_published', '=', True)]
        
        if category:
            domain.append(('category', '=', category))
        
        stories = request.env['success.story'].sudo().search(domain, order='publication_date desc')
        
        # Get all categories for filter
        all_categories = request.env['success.story'].sudo().search([
            ('is_published', '=', True)
        ]).mapped('category')
        categories = list(set(all_categories))
        categories.sort()
        
        values = {
            'stories': stories,
            'categories': categories,
            'current_category': category,
        }
        
        return request.render('success_stories_builder.success_stories_list_page', values)
    
    @http.route(['/success-stories/get-stories'], type='json', auth='public', website=True)
    def get_success_stories_json(self, category=None, limit=10, **kwargs):
        """
        JSON endpoint to fetch success stories for AJAX requests (used by slider snippet)
        """
        domain = [('is_published', '=', True)]
        
        if category and category != 'all':
            domain.append(('category', '=', category))
        
        stories = request.env['success.story'].sudo().search(domain, limit=int(limit), order='publication_date desc')
        
        result = []
        for story in stories:
            result.append({
                'id': story.id,
                'name': story.name,
                'client_name': story.client_id.name,
                'category': story.category,
                'short_description': story.short_description,
                'logo': f'/web/image/success.story/{story.id}/logo' if story.logo else False,
                'main_image': f'/web/image/success.story/{story.id}/main_image' if story.main_image else False,
                'url': story.website_url,
            })
        
        return result

