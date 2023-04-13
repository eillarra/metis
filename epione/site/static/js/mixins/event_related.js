var EventRelatedMixin = {
  data: function () {
    return {
      tmpObj: null,
      createUrl: null,
      stateVar: null,
      saveEventName: null,
      confirmRemoveMsg: 'Are you sure you want to delete this item?'
    }
  },
  methods: {
    clearObj: function () {
      this.tmpObj = null;
    },
    cloneObj: function (obj) {
      this.tmpObj = JSON.parse(JSON.stringify(obj));
    },
    createOrUpdate: function (obj) {
      var self = this;

      if (_.has(obj, 'self')) {
        Epione.api.update(obj, function (res) {
          self.$store.commit('update', {var: self.stateVar, action: 'update', obj: res.data});
          EventEmitter.emit('epione-editor-hide-after-save');
        });
      } else {
        Epione.api.create(this.createUrl, obj, function (res) {
          self.$store.commit('update', {var: self.stateVar, action: 'add', obj: res.data});
          EventEmitter.emit('epione-editor-hide-after-save');
        });
      }
    },
    remove: function (obj) {
      var self = this;
      Epione.utils.confirmAction(this.confirmRemoveMsg, function () {
        Epione.api.remove(obj, function (res) {
          self.$store.commit('update', {var: self.stateVar, action: 'remove', obj: obj});
        });
      });
    }
  },
  created: function () {
    EventEmitter.on(this.saveEventName, this.createOrUpdate);
    EventEmitter.on('epione-editor-hide', this.clearObj);
  },
  beforeUnmount: function () {
    EventEmitter.off(this.saveEventName);
    EventEmitter.off('epione-editor-hide');
  }
};
