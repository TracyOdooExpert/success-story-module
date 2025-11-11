/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.SuccessStoriesSlider = publicWidget.Widget.extend({
    selector: '.s_success_stories_slider',
    events: {
        'click .slider-arrow-prev': '_onPrevClick',
        'click .slider-arrow-next': '_onNextClick',
        'click .success-stories-filter button': '_onFilterClick',
    },

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this.currentIndex = 0;
        this.itemsToShow = parseInt(this.$el.attr('data-items-to-show') || this.$el.attr('data-itemsToShow')) || 4;
        this.itemsLimit = parseInt(this.$el.find('.success-stories-slider').attr('data-limit') || this.$el.attr('data-itemsLimit')) || 10;
        this.currentCategory = this.$el.attr('data-category') || 'all';
        if (this.$el.attr('data-category')) {
            this.$el.find('.success-stories-filter').hide();
        }
        this._loadStories();
        this._setupResponsive();
    },

    /**
     * Load stories from server
     */
    _loadStories: function () {
        const self = this;

        rpc('/success-stories/get-stories', {
            category: this.currentCategory,
            limit: this.itemsLimit,
        }).then(function (stories) {
            self._renderStories(stories);
            self._loadCategories();
        });
    },

    /**
     * Load available categories
     */
    _loadCategories: function () {
        const self = this;

        rpc('/success-stories/get-stories', {
            category: null,
            limit: 100,
        }).then(function (stories) {
            const categories = [...new Set(stories.map(s => s.category))].sort();
            self._renderCategoryFilter(categories);
        });
    },

    /**
     * Render category filter buttons
     */
    _renderCategoryFilter: function (categories) {
        const $filterContainer = this.$('.success-stories-filter');
        const $allButton = $filterContainer.find('[data-category="all"]');
        
        // Remove existing category buttons (keep "All" button)
        $filterContainer.find('[data-category]:not([data-category="all"])').remove();
        
        // Add category buttons
        categories.forEach(category => {
            const $button = $('<button/>', {
                type: 'button',
                class: 'btn btn-outline-primary',
                'data-category': category,
                text: category,
            });
            $filterContainer.append($button);
        });
    },

    /**
     * Render stories in the slider
     */
    _renderStories: function (stories) {
        const $slider = this.$('.success-stories-slider');
        $slider.empty();

        if (stories.length === 0) {
            $slider.append('<div class="col-12 text-center p-5"><p>No success stories found.</p></div>');
            return;
        }

        stories.forEach(story => {
            const $card = this._createStoryCard(story);
            $slider.append($card);
        });

        this.totalItems = stories.length;
        this.currentIndex = 0;
        this._updateSliderPosition();
        this._updateArrows();
    },

    /**
     * Create a story card element
     */
    _createStoryCard: function (story) {
        const $card = $('<div/>', {
            class: 'story-card flex-shrink-0',
        });

        const imageUrl = story.main_image || story.logo || '/web/static/img/placeholder.png';
        
        const cardHtml = `
            <div class="card h-100 shadow-sm">
                <img src="${imageUrl}" class="card-img-top" alt="${story.name}" style="height: 200px; object-fit: cover;">
                <div class="card-body d-flex flex-column">
                    ${story.logo ? `<div class="mb-2"><img src="${story.logo}" alt="${story.client_name}" style="max-height: 40px;"></div>` : ''}
                    <h5 class="card-title">${story.name}</h5>
                    <p class="card-text text-muted small">${story.category}</p>
                    <p class="card-text flex-grow-1">${story.short_description ? story.short_description.substring(0, 100) + '...' : ''}</p>
                    <a href="${story.url}" class="btn btn-primary mt-auto">Read More</a>
                </div>
            </div>
        `;

        $card.html(cardHtml);
        return $card;
    },

    /**
     * Update slider position
     */
    _updateSliderPosition: function () {
        const $slider = this.$('.success-stories-slider');
        const cardWidth = this.$('.story-card').first().outerWidth(true) || 300;
        const offset = -this.currentIndex * cardWidth;
        $slider.css('transform', `translateX(${offset}px)`);
    },

    /**
     * Update arrow visibility
     */
    _updateArrows: function () {
        const maxIndex = Math.max(0, this.totalItems - this.itemsToShow);
        
        this.$('.slider-arrow-prev').toggleClass('disabled', this.currentIndex <= 0);
        this.$('.slider-arrow-next').toggleClass('disabled', this.currentIndex >= maxIndex);
    },

    /**
     * Setup responsive behavior
     */
    _setupResponsive: function () {
        const self = this;
        
        $(window).on('resize.success_stories_slider', function () {
            self._updateResponsiveItems();
            self._updateSliderPosition();
            self._updateArrows();
        });
        
        this._updateResponsiveItems();
    },

    /**
     * Update items to show based on screen size
     */
    _updateResponsiveItems: function () {
        const width = $(window).width();
        
        if (width < 768) {
            this.itemsToShow = 1;
        } else if (width < 992) {
            this.itemsToShow = 2;
        } else if (width < 1200) {
            this.itemsToShow = 3;
        } else {
            this.itemsToShow = parseInt(this.$el.attr('data-items-to-show') || this.$el.attr('data-itemsToShow')) || 4;
        }
    },

    /**
     * Handle previous button click
     */
    _onPrevClick: function (ev) {
        ev.preventDefault();
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this._updateSliderPosition();
            this._updateArrows();
        }
    },

    /**
     * Handle next button click
     */
    _onNextClick: function (ev) {
        ev.preventDefault();
        const maxIndex = Math.max(0, this.totalItems - this.itemsToShow);
        if (this.currentIndex < maxIndex) {
            this.currentIndex++;
            this._updateSliderPosition();
            this._updateArrows();
        }
    },

    /**
     * Handle filter button click
     */
    _onFilterClick: function (ev) {
        ev.preventDefault();
        const $button = $(ev.currentTarget);
        const category = $button.data('category');
        
        // Update active state
        this.$('.success-stories-filter button').removeClass('active');
        $button.addClass('active');
        
        // Load stories for selected category
        this.currentCategory = category === 'all' ? null : category;
        this._loadStories();
    },

    /**
     * @override
     */
    destroy: function () {
        $(window).off('resize.success_stories_slider');
        this._super.apply(this, arguments);
    },
});

export default publicWidget.registry.SuccessStoriesSlider;

