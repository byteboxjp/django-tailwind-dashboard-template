/**
 * Alpine.js グローバルストア
 */
document.addEventListener('alpine:init', () => {
    // ダークモードストア
    Alpine.store('darkMode', {
        on: false,
        
        init() {
            // ローカルストレージまたはシステム設定から初期値を取得
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                this.on = savedTheme === 'dark';
            } else if (window.matchMedia) {
                this.on = window.matchMedia('(prefers-color-scheme: dark)').matches;
            }
            this.update();
        },
        
        toggle() {
            this.on = !this.on;
            this.update();
        },
        
        update() {
            localStorage.setItem('theme', this.on ? 'dark' : 'light');
            if (this.on) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
        }
    });
    
    // サイドバーストア
    Alpine.store('sidebar', {
        open: false,
        
        toggle() {
            this.open = !this.open;
        },
        
        close() {
            this.open = false;
        }
    });
    
    // 通知ストア
    Alpine.store('notifications', {
        items: [],
        
        add(message, type = 'info') {
            const id = Date.now();
            this.items.push({
                id,
                message,
                type,
                timestamp: new Date()
            });
            
            // 5秒後に自動削除
            setTimeout(() => {
                this.remove(id);
            }, 5000);
        },
        
        remove(id) {
            this.items = this.items.filter(item => item.id !== id);
        }
    });
});

// Alpine.js グローバル関数
document.addEventListener('alpine:init', () => {
    // フォーマット関数
    Alpine.data('formatters', () => ({
        // 数値をカンマ区切りでフォーマット
        formatNumber(num) {
            return new Intl.NumberFormat('ja-JP').format(num);
        },
        
        // 日付をフォーマット
        formatDate(date, format = 'short') {
            const d = new Date(date);
            const options = {
                short: { year: 'numeric', month: 'short', day: 'numeric' },
                long: { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' },
                time: { hour: '2-digit', minute: '2-digit' }
            };
            return d.toLocaleDateString('ja-JP', options[format] || options.short);
        }
    }));
    
    // ドロップダウンコンポーネント
    Alpine.data('dropdown', () => ({
        open: false,
        
        toggle() {
            this.open = !this.open;
        },
        
        close() {
            this.open = false;
        },
        
        init() {
            // クリック外で閉じる
            this.$watch('open', (value) => {
                if (value) {
                    this.$nextTick(() => {
                        document.addEventListener('click', this.handleOutsideClick);
                    });
                } else {
                    document.removeEventListener('click', this.handleOutsideClick);
                }
            });
        },
        
        handleOutsideClick(event) {
            if (!this.$el.contains(event.target)) {
                this.close();
            }
        }
    }));
    
    // モーダルコンポーネント
    Alpine.data('modal', () => ({
        open: false,
        
        show() {
            this.open = true;
            document.body.style.overflow = 'hidden';
        },
        
        hide() {
            this.open = false;
            document.body.style.overflow = '';
        },
        
        toggle() {
            this.open ? this.hide() : this.show();
        }
    }));
});

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // ダークモードの初期化（Alpine.js初期化前）
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    }
});

// システムのカラースキーム変更を監視
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            Alpine.store('darkMode').on = e.matches;
            Alpine.store('darkMode').update();
        }
    });
}