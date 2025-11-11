# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
from datetime import date


class SuccessStory(models.Model):
    _name = 'success.story'
    _description = 'Success Story / Testimonial'
    _inherit = ['website.seo.metadata', 'website.published.mixin']
    _order = 'publication_date desc, id desc'

    # Basic Information
    name = fields.Char(
        string='Title',
        required=True,
        translate=True,
        help='Title of the success story'
    )
    
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        domain=[('is_company', '=', True)],
        help='Select the client/company for this success story'
    )

    category = fields.Char(
        string='Category',
        required=True,
        help='Category for filtering (e.g., Technology, Healthcare, Finance)'
    )

    publication_date = fields.Date(
        string='Publication Date',
        default=fields.Date.context_today,
        required=True,
        help='Date when the story was/will be published'
    )

    # Images and Media
    logo = fields.Binary(
        string='Logo',
        attachment=True,
        help='Client logo image'
    )

    logo_filename = fields.Char(string='Logo Filename')

    main_image = fields.Binary(
        string='Main Image',
        attachment=True,
        required=True,
        help='Main featured image for the success story'
    )

    main_image_filename = fields.Char(string='Main Image Filename')

    # 4 Extra Images
    extra_image_1 = fields.Binary(
        string='Extra Image 1',
        attachment=True
    )
    extra_image_1_filename = fields.Char(string='Extra Image 1 Filename')

    extra_image_2 = fields.Binary(
        string='Extra Image 2',
        attachment=True
    )
    extra_image_2_filename = fields.Char(string='Extra Image 2 Filename')

    extra_image_3 = fields.Binary(
        string='Extra Image 3',
        attachment=True
    )
    extra_image_3_filename = fields.Char(string='Extra Image 3 Filename')

    extra_image_4 = fields.Binary(
        string='Extra Image 4',
        attachment=True
    )
    extra_image_4_filename = fields.Char(string='Extra Image 4 Filename')

    # Video
    video_url = fields.Char(
        string='Video URL',
        help='YouTube video link (e.g., https://www.youtube.com/watch?v=xxxxx)'
    )
    
    video_embed_code = fields.Char(
        string='Video Embed Code',
        compute='_compute_video_embed_code',
        store=True,
        help='Automatically generated embed code from YouTube URL'
    )

    # Text Content
    short_description = fields.Text(
        string='Short Description',
        translate=True,
        required=True,
        help='Brief description for cards and previews (max 300 characters recommended)'
    )

    main_text = fields.Html(
        string='Main Text',
        translate=True,
        required=True,
        sanitize_attributes=False,
        sanitize_form=False,
        help='Main content of the success story (long text with HTML formatting)'
    )

    # 5 Extra Text Fields
    extra_text_1 = fields.Html(
        string='Extra Text 1',
        translate=True,
        sanitize_attributes=False,
        sanitize_form=False
    )

    extra_text_2 = fields.Html(
        string='Extra Text 2',
        translate=True,
        sanitize_attributes=False,
        sanitize_form=False
    )

    extra_text_3 = fields.Html(
        string='Extra Text 3',
        translate=True,
        sanitize_attributes=False,
        sanitize_form=False
    )

    extra_text_4 = fields.Html(
        string='Extra Text 4',
        translate=True,
        sanitize_attributes=False,
        sanitize_form=False
    )

    extra_text_5 = fields.Html(
        string='Extra Text 5',
        translate=True,
        sanitize_attributes=False,
        sanitize_form=False
    )

    # Product Link (CTA)
    product_id = fields.Many2one(
        'product.template',
        string='Related Product',
        help='Link to a product to display as CTA on the website'
    )

    product_link_text = fields.Char(
        string='Product Link Text',
        default='View Product',
        translate=True,
        help='Text for the product CTA button'
    )

    product_link_url = fields.Char(
        string='Product URL',
        compute='_compute_product_link_url',
        help='Automatically generated product URL'
    )

    # Website and SEO
    website_url = fields.Char(
        string='Website URL',
        compute='_compute_website_url',
        store=True,
        help='Unique URL for this success story page'
    )

    url_slug = fields.Char(
        string='URL Slug',
        compute='_compute_url_slug',
        store=True,
        help='SEO-friendly URL slug'
    )

    # Computed Fields
    is_published_website = fields.Boolean(
        string='Published on Website',
        related='is_published',
        readonly=False,
        help='Check to publish this story on the website'
    )

    @api.depends('video_url')
    def _compute_video_embed_code(self):
        """Extract YouTube video ID and generate embed code"""
        for record in self:
            if record.video_url:
                # Extract YouTube video ID from various URL formats
                video_id = None
                patterns = [
                    r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
                    r'youtube\.com\/embed\/([^&\n?#]+)',
                ]

                for pattern in patterns:
                    match = re.search(pattern, record.video_url)
                    if match:
                        video_id = match.group(1)
                        break

                if video_id:
                    record.video_embed_code = 'https://www.youtube.com/embed/%s' % video_id
                else:
                    record.video_embed_code = False
            else:
                record.video_embed_code = False

    @api.depends('product_id')
    def _compute_product_link_url(self):
        """Generate product URL"""
        for record in self:
            if record.product_id:
                record.product_link_url = '/shop/product/%s' % record.product_id.id
            else:
                record.product_link_url = False

    @api.depends('name')
    def _compute_url_slug(self):
        """Generate SEO-friendly URL slug"""
        for record in self:
            if record.name:
                # Convert to lowercase and replace spaces with hyphens
                slug = record.name.lower()
                # Remove special characters
                slug = re.sub(r'[^a-z0-9\s-]', '', slug)
                # Replace spaces with hyphens
                slug = re.sub(r'[\s]+', '-', slug)
                # Remove multiple hyphens
                slug = re.sub(r'-+', '-', slug)
                # Remove leading/trailing hyphens
                slug = slug.strip('-')

                # Add ID to ensure uniqueness (only for saved records)
                if record.id and isinstance(record.id, int):
                    record.url_slug = '%s-%s' % (slug, record.id)
                else:
                    record.url_slug = slug
            else:
                record.url_slug = False

    @api.depends('url_slug')
    def _compute_website_url(self):
        """Generate full website URL"""
        for record in self:
            if record.url_slug:
                record.website_url = '/success-story/%s' % record.url_slug
            else:
                record.website_url = False

    @api.constrains('short_description')
    def _check_short_description_length(self):
        """Validate short description length"""
        for record in self:
            if record.short_description and len(record.short_description) > 300:
                raise ValidationError(_('Short description should not exceed 300 characters for better display in cards.'))

    def action_publish(self):
        """Publish the success story"""
        self.ensure_one()
        self.is_published = True
        return True

    def action_unpublish(self):
        """Unpublish the success story"""
        self.ensure_one()
        self.is_published = False
        return True

    def get_backend_menu_id(self):
        """Get the menu ID for backend access"""
        return self.env.ref('success_stories_builder.menu_success_stories_root').id
