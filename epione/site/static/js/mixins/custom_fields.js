var CustomFieldsMixin = {
  data: function () {
    return {
      module: 'default',
      createUrl: null,
      fieldsetTarget: null,
      obj: null
    };
  },
  computed: _.extend(
    Vuex.mapState(['event']), {
    replaceMainForm: function () {
      if (!this.event || !_.has(this.event.custom_fields, this.module)) return false;
      return this.event.custom_fields[this.module].replace;
    },
    target: function () {
      return this.fieldsetTarget;
    },
    fieldsets: function () {
      if (!this.event || !_.has(this.event.custom_fields, this.module)) return null;
      if (!_.has(this.event.custom_fields[this.module], 'fieldsets')) return [];

      if (this.target) {
        var target = this.target;
        return this.event.custom_fields[this.module].fieldsets.filter(function (fs) {
          return fs.target.indexOf(target) !== -1;
        });
      }

      return this.event.custom_fields[this.module].fieldsets;
    },
    customFormIsValid: function () {
      var obj = this.obj;
      var errors = [];

      if (this.obj) {
        _.each(this.fieldsets, function (fieldset) {
          _.each(fieldset.fields, function (f) {
            if (
              (f.required && (!_.has(obj.custom_data, f.id) || _.isEmpty(obj.custom_data[f.id])))
              || (f.mandatory && _.has(obj.custom_data, f.id) && obj.custom_data[f.id] === false)
            ) {
              errors.push(true);
            }
          });
        });
      }

      return !_.contains(errors, true);
    },
    formIsValid: function () {
      return this.customFormIsValid;
    }
  }),
  methods: {
    cleanObj: function (obj) {
      return obj;
    },
    createOrUpdate: function (obj) {
      var self = this;
      var obj = this.cleanObj(obj);

      if (_.has(obj, 'self')) {
        Epione.api.update(obj, function (res) {
          self.obj = res.data;
        });
      } else {
        Epione.api.create(this.createUrl, obj, function (res) {
          window.history.pushState('', '', res.data.url + self.$route.href);
          window.scrollTo(0, 0);
          self.obj = res.data;
        });
      }
    },
    fixObj: function () {
      var self = this;

      if (!this.event || !this.obj) {
        setTimeout(function () { self.fixObj(); }, 25);
        return;
      };

      if (this.fieldsets.length) {
        _.each(this.fieldsets, function (fieldset) {
          _.each(fieldset.fields, function (f) {
            if (!_.has(self.obj.custom_data, f.id)) {
              self.obj.custom_data[f.id] = {
                'text': null,
                'text_list': [],
                'single_choice': null,
                'multiple_choice': [],
                'checkbox': f.default
              }[f.type];
            }
          });
        });
      }
    }
  },
  created: function () {
    this.fixObj();
  }
};
