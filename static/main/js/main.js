(function (window, document, undefined) {
    'use strict';

    if (document.querySelector('.header')) {
        const headerBtn = document.querySelector('.header__btn');
        const headerNav = document.querySelector('.menu');

        function toggleHeaderMenu() {
            headerBtn.classList.toggle('header__btn--active');
            headerNav.classList.toggle('menu--active');
        }

        headerBtn.addEventListener('click', toggleHeaderMenu);
    }

    if (document.querySelector('.mfilter')) {
        const mfilterBtn = document.querySelector('.filter__menu');
        const mfilterClose = document.querySelector('.mfilter__close');
        const mfilter = document.querySelector('.mfilter');

        function toggleMfilter() {
            mfilter.classList.toggle('mfilter--active');
        }

        mfilterBtn.addEventListener('click', toggleMfilter);
        mfilterClose.addEventListener('click', toggleMfilter);
    }

    const splideConfig = {
        type: 'loop',
        drag: true,
        speed: 800,
        gap: 24,
        arrows: false,
        focus: 0
    };

    if (document.querySelector('.home__carousel')) {
        new Splide('.home__carousel', {
            ...splideConfig,
            perPage: 5,
            pagination: false,
            breakpoints: {
                575: { perPage: 2, pagination: true },
                767: { perPage: 3, pagination: true },
                991: { perPage: 3, pagination: true },
                1199: { perPage: 4, pagination: true },
                1399: { perPage: 5, pagination: true }
            }
        }).mount();
    }

    if (document.querySelector('.hero')) {
        new Splide('.hero', {
            ...splideConfig,
            perPage: 1,
            pagination: true,
            speed: 1200,
            gap: 24,
            breakpoints: {
                767: { gap: 20 },
                1199: { gap: 24 }
            }
        }).mount();
    }

    if (document.querySelector('.section__carousel')) {
        const elms = document.getElementsByClassName('section__carousel');
        for (let i = 0; i < elms.length; i++) {
            new Splide(elms[i], {
                ...splideConfig,
                perPage: 6,
                pagination: false,
                breakpoints: {
                    575: { perPage: 2, pagination: true },
                    767: { perPage: 3, pagination: true },
                    991: { perPage: 3, pagination: true },
                    1199: { perPage: 4, pagination: true }
                }
            }).mount();
        }
    }

    if (document.querySelector('.section__roadmap')) {
        const elms = document.getElementsByClassName('section__roadmap');
        for (let i = 0; i < elms.length; i++) {
            new Splide(elms[i], {
                ...splideConfig,
                perPage: 3,
                autoHeight: true,
                pagination: false,
                gap: 30,
                breakpoints: {
                    767: { perPage: 1, gap: 20, pagination: true },
                    991: { perPage: 2, pagination: true },
                    1199: { perPage: 3, pagination: true }
                }
            }).mount();
        }
    }

    const setBackground = (selector) => {
        const element = document.querySelector(selector);
        if (element && element.getAttribute('data-bg')) {
            element.style.background = `url(${element.getAttribute('data-bg')}) center center / cover no-repeat`;
        }
    };

    setBackground('.section--bg');
    setBackground('.section__details-bg');

    if (document.querySelector('.hero__slide')) {
        document.querySelectorAll('.hero__slide').forEach(element => {
            if (element.getAttribute('data-bg')) {
                element.style.background = `url(${element.getAttribute('data-bg')}) center center / cover no-repeat`;
            }
        });
    }

    const scrollSelectors = [
        '.dashbox__table-wrap--1',
        '.dashbox__table-wrap--2',
        '.item__description--details'
    ];

    scrollSelectors.forEach(selector => {
        if (document.querySelector(selector)) {
            Scrollbar.init(document.querySelector(selector), {
                damping: 0.1,
                renderByPixels: true,
                alwaysShowTracks: true,
                continuousScrolling: true
            });
        }
    });

    const slimSelectConfig = {
        '#filter__genre': {},
        '#filter__quality': { settings: { showSearch: false } },
        '#filter__rate': { settings: { showSearch: false } },
        '#filter__sort': { settings: { showSearch: false } },
        '#mfilter__genre': {},
        '#mfilter__quality': { settings: { showSearch: false } },
        '#mfilter__rate': { settings: { showSearch: false } },
        '#mfilter__sort': { settings: { showSearch: false } },
        '#filter__series': { settings: { showSearch: false } },
        '#filter__sync': { settings: { showSearch: false } }
    };

    Object.keys(slimSelectConfig).forEach(selector => {
        if (document.querySelector(selector)) {
            new SlimSelect({
                select: selector,
                ...slimSelectConfig[selector]
            });
        }
    });
    
    if (document.querySelector('#plan-modal')) {
        const myModalEl = document.getElementById('plan-modal');
        myModalEl.addEventListener('show.bs.modal', () => {
            if (window.innerWidth > 1200) {
                const header = document.querySelector('.header');
                const scrollBarWidth = window.innerWidth - document.documentElement.clientWidth;
                header.style.paddingRight = `${scrollBarWidth}px`;
            }
        });

        myModalEl.addEventListener('hidden.bs.modal', () => {
            if (window.innerWidth > 1200) {
                const header = document.querySelector('.header');
                header.style.paddingRight = '';
            }
        });
    }

    if (document.querySelector('#player')) {
        new Plyr(document.querySelector('#player'));
    }

    if (document.querySelector('.gallery')) {
        const initPhotoSwipeFromDOM = (gallerySelector) => {
            const parseThumbnailElements = (el) => {
                const thumbElements = el.childNodes;
                const items = [];

                thumbElements.forEach((figureEl) => {
                    if (figureEl.nodeType !== 1) return;

                    const linkEl = figureEl.children[0];
                    const size = linkEl.getAttribute('data-size').split('x');

                    const item = {
                        src: linkEl.getAttribute('href'),
                        w: parseInt(size[0], 10),
                        h: parseInt(size[1], 10)
                    };

                    if (figureEl.children.length > 1) {
                        item.title = figureEl.children[1].innerHTML;
                    }

                    if (linkEl.children.length > 0) {
                        item.msrc = linkEl.children[0].getAttribute('src');
                    }

                    item.el = figureEl;
                    items.push(item);
                });

                return items;
            };

            const closest = (el, fn) => el && (fn(el) ? el : closest(el.parentNode, fn));
            const onThumbnailsClick = (e) => {
                e.preventDefault();
                const eTarget = e.target || e.srcElement;
                const clickedListItem = closest(eTarget, (el) => el.tagName && el.tagName.toUpperCase() === 'FIGURE');

                if (!clickedListItem) return false;

                const clickedGallery = clickedListItem.parentNode;
                const childNodes = clickedGallery.childNodes;
                let index;

                childNodes.forEach((childNode, nodeIndex) => {
                    if (childNode.nodeType === 1 && childNode === clickedListItem) {
                        index = nodeIndex;
                    }
                });

                if (index >= 0) {
                    openPhotoSwipe(index, clickedGallery);
                }
                return false;
            };

            const photoswipeParseHash = () => {
                const hash = window.location.hash.substring(1);
                const params = {};

                if (hash.length < 5) return params;

                const vars = hash.split('&');
                vars.forEach((pairStr) => {
                    const pair = pairStr.split('=');
                    if (pair.length >= 2) {
                        params[pair[0]] = pair[1];
                    }
                });

                if (params.gid) {
                    params.gid = parseInt(params.gid, 10);
                }

                return params;
            };

            const openPhotoSwipe = (index, galleryElement, disableAnimation = false, fromURL = false) => {
                const pswpElement = document.querySelectorAll('.pswp')[0];
                const items = parseThumbnailElements(galleryElement);

                const options = {
                    galleryUID: galleryElement.getAttribute('data-pswp-uid'),
                    getThumbBoundsFn: (index) => {
                        const thumbnail = items[index].el.getElementsByTagName('img')[0];
                        const pageYScroll = window.pageYOffset || document.documentElement.scrollTop;
                        const rect = thumbnail.getBoundingClientRect();

                        return { x: rect.left, y: rect.top + pageYScroll, w: rect.width };
                    },
                    index: fromURL ? parseInt(index, 10) - 1 : index,
                    showAnimationDuration: disableAnimation ? 0 : undefined
                };

                if (isNaN(options.index)) return;

                const gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
                gallery.init();
            };

            const galleryElements = document.querySelectorAll(gallerySelector);

            galleryElements.forEach((galleryElement, i) => {
                galleryElement.setAttribute('data-pswp-uid', i + 1);
                galleryElement.onclick = onThumbnailsClick;
            });

            const hashData = photoswipeParseHash();
            if (hashData.pid && hashData.gid) {
                openPhotoSwipe(hashData.pid, galleryElements[hashData.gid - 1], true, true);
            }
        };
        initPhotoSwipeFromDOM('.gallery');
    }
})(window, document);
