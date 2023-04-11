var CommonMarkReader = new commonmark.Parser({safe: true, smart: true});
var CommonMarkWriter = new commonmark.HtmlRenderer();


var SpartaCommonComponents = {

    'version-hash': {
    data: function () {
      return {
        rev: document.querySelector('html').dataset.rev || 'revhash'
      };
    },
    props: {
      size: {
        type: Number,
        default: 7
      }
    },
    template: '<span>{{ hash }}</span>',
    computed: {
      hash: function () {
        return this.rev.slice(0, this.size);
      }
    }
  },

  'django-form-error': {
    props: {
      field: {
        type: String,
        default: null
      },
      error: {
        type: String,
        required: true
      }
    },
    template: '<em class="hidden"></em>',
    created: function () {
      Quasar.Notify.create({
        timeout: 10000,
        progress: true,
        html: true,
        message: (this.field)
          ? '<strong>' + this.field + '</strong>: ' + this.error
          : this.error,
        type: 'negative',
        actions: [
          { label: 'Dismiss', color: 'white', handler: function () {} }
        ],
        attrs: {
          role: 'alert'
        }
      });
    }
  },

  'django-message': {
    props: {
      message: {
        type: String
      },
      level: {
        type: String
      },
      tags: {
        type: String
      }
    },
    template: '<em class="hidden"></em>',
    created: function () {
      /*
      DEBUG = 10
      INFO = 20
      SUCCESS = 25
      WARNING = 30
      ERROR = 40
      */
      var level = +this.level;
      Quasar.Notify.create({
        timeout: (level > 25) ? 10000 : 5000,
        message: this.message,
        type: {
          10: 'info',
          20: 'info',
          25: 'positive',
          30: 'warning',
          40: 'negative'
        }[level] || 'info',
        actions: [
          {
            label: 'Dismiss',
            color: (level == 30) ? 'dark' : 'white',
            handler: function () {}
          }
        ],
        attrs: {
          role: 'alert'
        }
      });
    }
  },

  'country-flag': {
    props: {
      code: {
        type: String
      }
    },
    template: '<i :class="css"></i>',
    computed: {
      css: function () {
        if (!this.code) return '';
        return [
          "flag-sprite",
          "flag-" + this.code[0],
          "flag-_" + this.code[1],
        ].join(' ').toLowerCase()
      }
    }
  },

  'display-3': {
    template: '<h5 class="q-mt-none q-mb-md text-weight-light"><slot></slot></h5>'
  },

  'display-5': {
    template: '<h6 class="q-mt-sm q-mb-lg text-weight-bold"><slot></slot></h6>'
  },

  'marked': {
    props: {
      text: {
        type: String,
        default: ''
      }
    },
    template: '<div class="marked" v-html="compiledText"></div>',
    computed: {
      compiledText: function () {
        if (!this.text || this.text == '') return this.text;
        return CommonMarkWriter.render(CommonMarkReader.parse(this.text));
      }
    }
  },

  'sparta-user-menu': {
    data: function () {
      return {
        userId: +(document.querySelector('html').dataset.user)
      };
    },
    props: {
      displayName: {
        type: String
      }
    },
    template: `
      <a v-if="userId > 0" class="cursor-pointer">
        <span v-show="$q.screen.gt.xs">{{ displayName }} &nbsp;<q-icon name="account_circle" size="xxs" />
        <q-menu anchor="top end" self="bottom right" :offset="[0, 8]">
          <q-list style="min-width: 140px">
            <q-item clickable tag="a" href="/">
              <q-item-section>Homepage</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable tag="a" href="/u/logout/">
              <q-item-section>Log out</q-item-section>
              <q-item-section side><q-icon name="logout" size="xs" /></q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </a>
    `
  },

  'sparta-no-data': {
    props: {
      message: {
        type: String,
        required: true
      },
      filter: {
        type: String,
        default: ''
      }
    },
    template: `
      <div class="full-width text-center q-pa-xl text-grey-6">
        <q-icon size="6em" :name="filter ? 'search_off' : 'layers_clear'" />
        <h5>{{ message }}</h5>
      </div>
    `
  },

  'google-logo': {
    template: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M113.47 309.408L95.648 375.94l-65.139 1.378C11.042 341.211 0 299.9 0 256c0-42.451 10.324-82.483 28.624-117.732h.014L86.63 148.9l25.404 57.644c-5.317 15.501-8.215 32.141-8.215 49.456.002 18.792 3.406 36.797 9.651 53.408z" fill="#fbbb00"/><path d="M507.527 208.176C510.467 223.662 512 239.655 512 256c0 18.328-1.927 36.206-5.598 53.451-12.462 58.683-45.025 109.925-90.134 146.187l-.014-.014-73.044-3.727-10.338-64.535c29.932-17.554 53.324-45.025 65.646-77.911h-136.89V208.176h245.899z" fill="#518ef8"/><path d="M416.253 455.624l.014.014C372.396 490.901 316.666 512 256 512c-97.491 0-182.252-54.491-225.491-134.681l82.961-67.91c21.619 57.698 77.278 98.771 142.53 98.771 28.047 0 54.323-7.582 76.87-20.818l83.383 68.262z" fill="#28b446"/><path d="M419.404 58.936l-82.933 67.896C313.136 112.246 285.552 103.82 256 103.82c-66.729 0-123.429 42.957-143.965 102.724l-83.397-68.276h-.014C71.23 56.123 157.06 0 256 0c62.115 0 119.068 22.126 163.404 58.936z" fill="#f14336"/></svg>
    `
  },

  'linkedin-logo': {
    template: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75.77 76.25"><path fill="#0077b5" d="M0 5.47C0 2.45 2.51 0 5.6 0h64.57c3.1 0 5.6 2.45 5.6 5.46v65.33c0 3.02-2.5 5.46-5.6 5.46H5.6c-3.09 0-5.6-2.44-5.6-5.46z"/><path fill="#fff" fill-rule="evenodd" d="M22.97 63.83V29.4H11.53v34.43zM17.25 24.7c3.99 0 6.47-2.64 6.47-5.95-.07-3.38-2.48-5.95-6.4-5.95-3.91 0-6.47 2.57-6.47 5.95 0 3.3 2.48 5.95 6.32 5.95zM29.3 63.83h11.45V44.6c0-1.03.07-2.05.37-2.79.83-2.05 2.71-4.18 5.87-4.18 4.15 0 5.8 3.15 5.8 7.78v18.42h11.45V44.09c0-10.58-5.65-15.5-13.18-15.5-6.17 0-8.88 3.45-10.39 5.8h.08V29.4H29.3c.15 3.23 0 34.43 0 34.43z"/></svg>
    `
  },

  'ugent-logo': {
    template: `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25.233 25.35"><path fill="#1e64c8" d="M12.197 9.822h1.479v9.608h-1.479zm-2.96 0h1.481v9.608H9.237Zm-2.96 0h1.479v9.608h-1.48Zm-2.96 0h1.48v9.608h-1.48Zm11.84 0h1.48v9.608h-1.48zm2.96 0h1.48v9.608h-1.478zm2.96 0h1.48v9.608h-1.48ZM1.801 20.912h22.273v1.48H1.8ZM22.556 8.34H3.316L1.839 6.86h22.2l-1.482 1.482M.322 23.869h25.23v1.481H.32Zm25.23-19.402L12.939 0 .32 4.467V6.04l12.613-4.467L25.551 6.04V4.467" /></svg>
    `
  },

  'socialaccount-provider': {
    props: {
      provider: {
        type: String,
        required: true
      },
      height: {
        type: String,
        default: '32px'
      }
    },
    template: `
      <component :is="comp" :style="{'height': height}"></component>
    `,
    computed: {
      comp: function () {
        var provider = this.provider.toLowerCase();
        if (provider == 'linkedin_oauth2') { provider = 'linkedin' };
        return provider + '-logo';
      }
    }
  },

  'sparta-copy-icon': {
    props: {
      text: {
        type: String,
        required: true
      }
    },
    template: '<q-icon name="copy_all" @click.stop="copyToClipboard" class="cursor-pointer" />',
    methods: {
      copyToClipboard: function () {
        Quasar.copyToClipboard(this.text).then(function () {
          Sparta.utils.notify('Copied to clipboard', 'none');
        }).catch(function () {
          Sparta.utils.notify('Could not copy to clipboard', 'warning');
        });
      }
    }
  },

  'sparta-contact-dialog': {
    data: function () {
      return {
        dialogVisible: false,
        user: null,
        msg: null
      };
    },
    props: {
      eventUrl: {
        type: String,
        required: true
      }
    },
    template: `
      <q-dialog v-model="showDialog" @show="dialogVisible = true">
        <q-card v-if="user" class="q-pa-sm" style="width: 500px">
          <q-toolbar>
            <q-toolbar-title class="q-ml-xs">Contact form</q-toolbar-title>
            <q-space />
            <q-btn v-close-popup flat round icon="close" />
          </q-toolbar>
          <q-card-section class="text-body2">
            <p>For privacy reasons we cannot share other users' emails. Please use this form to send a message to <strong>{{ user.name }}</strong><span v-if="user.affiliation"> ({{ user.affiliation }})</span>: we will share your email address with {{ user.name }} so you can get a direct response.</p>
            <q-input v-model="msg" filled type="textarea" class="q-mb-md"></q-input>
            <q-btn v-close-popup @click="sendMessage" outline color="primary" label="Send message" :disable="!msg" />
          </q-card-section>
          <q-card-section class="text-caption q-pb-lg">
            <span>Please note that {{ user.name }} can choose to discard your message.</span>
          </q-card-section>
        </q-card>
      </q-dialog>
    `,
    computed: {
      showDialog: {
        get: function () {
          return this.user != null;
        },
        set: function (val) {
          if (this.dialogVisible) {
            this.dialogVisible = false;
            this.msg = null;
            this.user = null;
          }
        }
      }
    },
    methods: {
      updateUser: function (user) {
        this.user = user;
      },
      sendMessage: function () {
        Sparta.api.request('post', this.eventUrl + 'contact/', {
          user_id: this.user.id,
          message: this.msg
        }).then(function (res) {
          Sparta.utils.notify('Message sent.');
        }).catch(function (error) {
          Sparta.utils.notifyApiError(error);
        });
      }
    },
    created: function () {
      EventEmitter.on('show-contact-dialog', this.updateUser);
    },
    beforeDestroy: function () {
      EventEmitter.off('show-contact-dialog');
    }
  },

  'sparta-search-bar': {
    emits: ['update:modelValue'],
    data: function () {
      return {
        dialogVisible: false,
        filterData: {}
      };
    },
    props: {
      modelValue: {
        type: String,
        default: ''
      },
      placeholder: {
        type: String,
        default: 'Search...'
      },
      filters: {
        type: Array,
        default: function () {
          return [];
        }
      }
    },
    template: `
      <div>
        <q-input filled :dense="$q.screen.gt.sm" v-model="q" :placeholder="placeholder" type="search" class="text-mono q-mb-md">
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
          <template v-slot:append>
            <q-icon v-show="q !== ''" @click="q = ''" name="close" class="cursor-pointer" />
            <q-icon v-if="filters.length" @click="dialogVisible = true" name="tune" class="cursor-pointer q-ml-sm" />
          </template>
        </q-input>
        <q-dialog v-model="dialogVisible" position="right" @before-show="updateFilters" @before-hide="updateQuery">
          <q-card v-if="filters.length" style="width: 280px; height: 100%" class="q-pa-lg">
            <display-5 class="text-grey-8">Search builder</display-5>
            <div class="q-gutter-md q-mt-md">
              <q-input dense filled v-model="filterData.text" @keyup.enter="dialogVisible = false" type="text" label="Text" />
              <q-separator />
              <q-select v-for="filter in filters" dense filled v-model="filterData[filter.name]" :options="filter.options" :label="filter.name">
                <template v-if="filterData[filter.name]" v-slot:append>
                  <q-icon name="clear" @click.stop="filterData[filter.name] = null" class="cursor-pointer" size="14px" />
                </template>
              </q-select>
            </div>
          </q-card>
        </q-dialog>
      </div>
    `,
    computed: {
      q: {
        get: function () {
          return this.modelValue;
        },
        set: function (val) {
          this.$emit('update:modelValue', val);
        }
      }
    },
    methods: {
      updateQuery: function () {
        var val = this.filterData;
        var q = [val.text];
        _.each(_.keys(val), function (k) {
          if (k != 'text' && val[k]) q.push(k + ':' + val[k]);
        });
        this.$emit('update:modelValue', q.join(' ').trim());
      },
      updateFilters: function () {
        var q = this.q.replace(/\s+/g,' ').trim();

        if (q == '') {
          this.filterData = {};
          return;
        };

        var filterParts = {};
        var textParts = [];

        _.each(q.split(' '), function (word) {
          if (word.indexOf(':') > -1) {
            var s = word.split(':');
            filterParts[s[0]] = s[1];
          } else {
            textParts.push(word);
          }
        });

        filterParts['text'] = textParts.join(' ');

        this.filterData = filterParts;
      }
    }
  },

  'stats-progress': {
    props: {
      size: {
        type: String,
        default: 'lg'
      },
      fontSize: {
        type: String,
        default: '12px'
      },
      value: {
        type: Number,
        required: true
      }
    },
    template: `
      <q-circular-progress show-value :size="size" :font-size="fontSize" :value="value" :color="color" track-color="grey-3">
        <samp><strong><slot></slot></strong></samp>
      </q-circular-progress>
    `,
    computed: {
      color: function () {
        if (this.value == 100) return 'positive';
        if (this.value >= 50) return 'blue';
        if (this.value >= 25) return 'light-blue';
        if (this.value >= 10) return 'cyan';
        return 'blue-grey';
      }
    }
  }

};
