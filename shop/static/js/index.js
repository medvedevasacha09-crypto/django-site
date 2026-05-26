/* ═══════════════════════════════════════════════
   FLUFFY — index.js
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

    // ─── 1. Автоматично ховати повідомлення ──────────────────────────────────
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 500);
        }, 3500);
    });


    // ─── 2. Мобільне меню (бургер) ───────────────────────────────────────────
    const burgerBtn = document.getElementById('burger-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (burgerBtn && mobileMenu) {
        burgerBtn.addEventListener('click', function () {
            const isOpen = mobileMenu.classList.toggle('open');
            burgerBtn.setAttribute('aria-expanded', isOpen);
            burgerBtn.textContent = isOpen ? '✕' : '☰';
        });

        // Закривати меню при кліку на посилання
        mobileMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                mobileMenu.classList.remove('open');
                burgerBtn.textContent = '☰';
            });
        });

        // Закривати при кліку поза меню
        document.addEventListener('click', function (e) {
            if (!mobileMenu.contains(e.target) && e.target !== burgerBtn) {
                mobileMenu.classList.remove('open');
                burgerBtn.textContent = '☰';
            }
        });
    }


    // ─── 3. Активне посилання в навігації ────────────────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });


    // ─── 4. Кошик — зміна кількості кнопками +/- ─────────────────────────────
    document.querySelectorAll('.cart-item').forEach(function (item) {
        const qtyInput = item.querySelector('.qty-input');
        const btnMinus = item.querySelector('.btn-minus');
        const btnPlus  = item.querySelector('.btn-plus');

        if (!qtyInput) return;

        if (btnMinus) {
            btnMinus.addEventListener('click', function () {
                const val = parseInt(qtyInput.value) || 1;
                if (val > 1) {
                    qtyInput.value = val - 1;
                    qtyInput.closest('form').submit();
                }
            });
        }
        if (btnPlus) {
            btnPlus.addEventListener('click', function () {
                const val = parseInt(qtyInput.value) || 1;
                qtyInput.value = val + 1;
                qtyInput.closest('form').submit();
            });
        }
    });


    // ─── 5. Підтвердження видалення з кошика ─────────────────────────────────
    document.querySelectorAll('.btn-remove').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm('Видалити товар з кошика?')) {
                e.preventDefault();
            }
        });
    });


    // ─── 6. Рейтинг — підсвічування зірок ────────────────────────────────────
    const ratingLabels = document.querySelectorAll('.rating-choices label');

    ratingLabels.forEach(function (label, index) {
        label.addEventListener('mouseenter', function () {
            ratingLabels.forEach(function (l, i) {
                l.style.transform = i <= index ? 'scale(1.3)' : 'scale(1)';
                l.style.filter    = i <= index ? 'brightness(1.2)' : 'brightness(0.7)';
            });
        });

        label.addEventListener('mouseleave', function () {
            ratingLabels.forEach(function (l) {
                l.style.transform = '';
                l.style.filter    = '';
            });
        });

        label.addEventListener('click', function () {
            ratingLabels.forEach(function (l, i) {
                l.style.transform = i <= index ? 'scale(1.2)' : 'scale(1)';
            });
        });
    });


    // ─── 7. Smooth scroll для якорів ─────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });


    // ─── 8. Lazy loading для картинок ────────────────────────────────────────
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imgObserver.unobserve(img);
                }
            });
        }, { rootMargin: '100px' });

        document.querySelectorAll('img[data-src]').forEach(function (img) {
            imgObserver.observe(img);
        });
    }


    // ─── 9. Анімація появи карток при скролі ─────────────────────────────────
    if ('IntersectionObserver' in window) {
        const cardObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    cardObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.hit-card, .cat-card, .delivery-card').forEach(function (card) {
            card.classList.add('fade-in-card');
            cardObserver.observe(card);
        });
    }


    // ─── 10. Валідація форми замовлення ──────────────────────────────────────
    const orderForm = document.querySelector('.order-form-box form');
    if (orderForm) {
        orderForm.addEventListener('submit', function (e) {
            const phone = orderForm.querySelector('[name="phone"]');
            if (phone) {
                const phoneVal = phone.value.trim();
                const phoneRegex = /^\+?380\d{9}$/;
                if (!phoneRegex.test(phoneVal.replace(/\s/g, ''))) {
                    e.preventDefault();
                    showFieldError(phone, 'Введіть номер у форматі +380XXXXXXXXX');
                    return;
                }
            }
        });
    }


    // ─── 11. Back to top кнопка ──────────────────────────────────────────────
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function () {
            backToTop.style.display = window.scrollY > 400 ? 'flex' : 'none';
        });
        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }


    // ─── Допоміжні функції ────────────────────────────────────────────────────
    function showFieldError(field, message) {
        removeFieldError(field);
        field.style.borderColor = 'var(--error)';
        const err = document.createElement('small');
        err.className = 'js-field-error';
        err.style.color = 'var(--error)';
        err.style.fontSize = '12px';
        err.style.marginTop = '4px';
        err.style.display = 'block';
        err.textContent = message;
        field.parentNode.appendChild(err);
        field.focus();
        field.addEventListener('input', function () { removeFieldError(field); }, { once: true });
    }

    function removeFieldError(field) {
        field.style.borderColor = '';
        const err = field.parentNode.querySelector('.js-field-error');
        if (err) err.remove();
    }

});