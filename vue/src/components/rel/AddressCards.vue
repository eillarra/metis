<style lang="scss">
.metis__dialog-geocode {
  height: 550px;

  .q-dialog__inner--minimized > & {
    width: 520px !important;
    max-width: 100vw;
  }
}
</style>

<template>
  <div v-if="loading" class="flex flex-center q-mt-xl">
    <q-spinner color="grey-3" size="4em" />
  </div>
  <div v-else class="row q-col-gutter-sm">
    <div v-for="address in addresses" :key="address.id" class="col-12 align-items-stretch">
      <q-card flat square bordered class="column full-height">
        <q-card-section>
          <q-item-label>{{ address.address }}</q-item-label>
          <q-item-label>{{ address.postcode }} {{ address.city }}</q-item-label>
        </q-card-section>
        <q-card-actions class="use-default-q-btn q-pa-md">
          <q-btn outline square @click="deleteAddress(address)" color="red" icon="delete_outline" size="sm" />
          <q-space />
          <q-btn unelevated square @click="obj = address" color="ugent" icon="edit" size="sm" />
        </q-card-actions>
      </q-card>
    </div>
    <div class="col-12">
      <div class="row justify-end">
        <div class="col-6 ugent__create-btn" :class="{ 'col-md-1': !inDialog, 'col-md-2': inDialog }">
          <q-btn
            unelevated
            color="blue-1"
            :label="$t('form.new')"
            icon="add"
            class="text-ugent full-width"
            @click="
              obj = {
                address: '',
                postcode: '',
                city: '',
              }
            "
          />
        </div>
      </div>
    </div>
    <q-dialog v-model="dialogVisible">
      <dialog-form :icon="obj.self ? 'map' : 'add'" :title="$t('address')" class="metis__dialog-geocode">
        <template #page>
          <q-stepper v-model="step" vertical flat color="ugent" animated keep-alive>
            <q-step :name="1" :title="$t('form.address.create.find')" icon="search" active-icon="search">
              <div class="q-gutter-sm q-mt-sm">
                <q-input dense type="text" v-model="obj.address" :label="$t('form.address.fields.address')" />
                <q-input dense type="text" v-model="obj.postcode" :label="$t('form.address.fields.postcode')" />
                <q-input dense type="text" v-model="obj.city" :label="$t('form.address.fields.city')" />
              </div>
              <q-stepper-navigation class="flex">
                <q-space />
                <q-btn
                  unelevated
                  @click="geocode"
                  color="ugent"
                  :label="$t('form.search')"
                  :disable="!obj.address || !obj.city"
                />
              </q-stepper-navigation>
            </q-step>
            <q-step :name="2" :title="$t('form.address.create.new')" icon="fmd_good" active-icon="fmd_good">
              <div v-if="features.length">
                {{ $t('form.address.create.choose_feature') }}
                <q-list class="q-mt-md">
                  <q-item dense v-for="feature in features" :key="feature.id" tag="label" class="q-pl-none q-py-none">
                    <q-item-section side>
                      <q-radio v-model="selectedFeature" :val="(feature as object)" />
                    </q-item-section>
                    <q-item-section>{{ feature.place_name_nl }}</q-item-section>
                  </q-item>
                </q-list>
              </div>
              <div v-else>
                {{ $t('form.address.create.no_results') }}
              </div>
            </q-step>
          </q-stepper>
        </template>
        <template #footer>
          <div v-if="step == 2" class="flex q-gutter-sm q-pa-lg">
            <q-btn unelevated @click="step = 1" color="blue-1" text-color="ugent" :label="$t('form.back')" />
            <q-space />
            <q-btn
              unelevated
              color="ugent"
              :label="$t('form.address.save')"
              @click="save"
              :disable="!selectedFeature"
            />
          </div>
        </template>
      </dialog-form>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { usePage } from '@inertiajs/vue3';

import { api, axios } from '@/axios';
import { confirm } from '@/dialog';
import { notify } from '@/notify';

import DialogForm from '@/components/forms/DialogForm.vue';

const { t } = useI18n();
const page = usePage();

const props = defineProps<{
  apiEndpoint: ApiEndpoint;
  inDialog?: boolean;
}>();

const accessToken = computed<string>(() => page.props.mapbox_token as string);
const loading = ref<boolean>(true);
const step = ref(1);
const addresses = ref<Address[]>([]);
const obj = ref<Address | null>(null);
const features = ref<object[]>([]);
const selectedFeature = ref<object | null>(null);

const dialogVisible = computed<boolean>({
  get() {
    return !!obj.value;
  },
  set(value) {
    if (!value) {
      obj.value = null;
    }
  },
});

onMounted(() => {
  api.get(props.apiEndpoint).then((response) => {
    addresses.value = response.data;
    loading.value = false;
  });
});

function geocode() {
  const q = `${obj.value?.address} ${obj.value?.postcode} ${obj.value?.city}`;
  axios
    .get(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(q)}.json`, {
      params: {
        access_token: accessToken.value,
        types: 'address',
        language: 'nl,en',
        limit: 5,
        country: 'BE,NL',
      },
    })
    .then((res) => {
      if (res.data.features.length && res.data.features[0].relevance === 1) {
        features.value = [res.data.features[0]];
      } else {
        features.value = res.data.features;
      }
      selectedFeature.value = null;
      step.value = 2;
    });
}

function getContext(key: string) {
  return selectedFeature.value?.context.find((c: any) => c.id.includes(key)) || null;
}

function save() {
  if (!selectedFeature.value) return;

  const data = {
    address: `${selectedFeature.value.text} ${selectedFeature.value.address || ''}`.trim(),
    city: getContext('locality')?.text || getContext('place')?.text,
    postcode: getContext('postcode')?.text,
    country: getContext('country')?.short_code.toUpperCase(),
    mapbox_feature: selectedFeature.value,
  };

  if (obj.value?.self) {
    api.put(obj.value?.self, data).then((response) => {
      addresses.value = addresses.value.map((address) => {
        if (address.id === response.data.id) {
          return response.data;
        }
        return address;
      });
      notify.success(t('form.address.saved'));
      reset();
    });
  } else {
    api.post(props.apiEndpoint, data).then((response) => {
      addresses.value.push(response.data);
      notify.success(t('form.address.create.success'));
      reset();
    });
  }
}

function deleteAddress(add) {
  if (add.self) {
    confirm(t('form.address.confirm_delete'), () => {
      api.delete(add.self).then(() => {
        addresses.value = addresses.value.filter((address) => address.id !== add.id);
        notify.success(t('form.address.deleted'));
        reset();
      });
    });
  }
}

function reset() {
  obj.value = null;
  step.value = 1;
  selectedFeature.value = null;
}
</script>
