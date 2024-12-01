<template>
    <div class="container" id="ageBox">
        <h3><strong>{{ userStore.profileData.nickname}}</strong>
            <span class="title">님만의 추천 상품</span>
        </h3>
        <h4 class="mb-2 mt-4"><strong>예금상품</strong></h4>
        <swiper
            :modules="modules"
            :slides-per-view="3"
            :space-between="20"
            navigation
            :pagination="{ clickable: true }"
            :autoplay="{ delay: 2000, disableOnInteraction: false }"
            @swiper="onSwiper"
            @slideChange="onSlideChange"
            @swiperprogress="onProgress"
            style="width: 100%;"
        >
            <swiper-slide v-for="product in recommendStore.PrivateProducts.slice(0,8)" :key="product.id" @click="addProductToCart(product)">
                <div class="product-card">
                    <span>
                        <img :src="bankimg(product)" alt="은행 사진" class="profile-preview" />
                        <strong style="color: black;">{{ product.kor_co_nm }}</strong> 
                    </span>
                    <hr class="mt-1">
                    <p>상품명:
                        <span>{{ product.fin_prdt_nm }}</span>
                    </p>
                    <p>저축 금리 유형명: 
                        <span>{{ product.best_option.intr_rate_type_nm}}</span>
                    </p>
                    <p>저축 금리 : 
                        <span>{{ product.best_option.intr_rate }}</span>
                    </p>
                    <p>저축기간: 
                        <span>{{ product.best_option.save_trm }}개월</span>
                    </p>
                </div>
            </swiper-slide>
        </swiper>
        <!-- <div v-for="product in recommendStore.PrivateProducts.slice(0,8)" :key="product.id" @click="addProductToCart(product)">
            
            <p>{{product.kor_co_nm}} : {{ product.fin_prdt_nm }}</p>
        </div> -->
        <h4 class="mb-2 mt-4"><strong>적금상품</strong></h4>
        <swiper
            :modules="modules"
            :slides-per-view="3"
            :space-between="20"
            navigation
            :pagination="{ clickable: true }"
            :autoplay="{ delay: 2000, disableOnInteraction: false }"
            @swiper="onSwiper"
            @slideChange="onSlideChange"
            @swiperprogress="onProgress"
            style="width: 100%;"
        >
            <swiper-slide v-for="product in recommendStore.PrivateProductsForSaving.slice(0,8)" :key="product.id" @click="addProductToCart(product)">
                <div class="product-card">
                    <span>
                        <img :src="bankimg(product)" alt="은행 사진" class="profile-preview" />
                        <strong style="color: black;">{{ product.kor_co_nm }}</strong> 
                    </span>
                    <hr class="mt-1">
                    <p>상품명:
                        <span>{{ product.fin_prdt_nm }}</span>
                    </p>
                    <p>저축 금리 유형명: 
                        <span>{{ product.best_option.intr_rate_type_nm}}</span>
                    </p>
                    <p>저축 금리 : 
                        <span>{{ product.best_option.intr_rate }}</span>
                    </p>
                    <p>저축기간: 
                        <span>{{ product.best_option.save_trm }}개월</span>
                    </p>
                </div>
            </swiper-slide>
        </swiper>
        <!-- <div v-for="product in recommendStore.PrivateProductsForSaving.slice(0,8)" :key="product.id" @click="addProductToCart(product)">
            
            <p>{{product.kor_co_nm}} : {{ product.fin_prdt_nm }}</p>
        </div> -->
    </div>
</template>


<script setup>
    import { ref, onMounted ,defineProps , defineEmits  } from 'vue'
    import { useUserStore } from "@/stores/userStore";
    import { useRecommendStore } from "@/stores/recommend"
    import { Swiper, SwiperSlide } from "swiper/vue"; 
    import { Navigation, Pagination, Scrollbar, A11y } from 'swiper/modules';
    import { register } from 'swiper/element/bundle';
    import "swiper/swiper-bundle.css";
    import 'swiper/css/navigation';
    import 'swiper/css/pagination';

    register();
    const recommendStore = useRecommendStore()
    const emit = defineEmits()
    const userStore = useUserStore()

    const props = defineProps({
        myCart: {
            type: Array,
            required: true
        }
    })

    function addProductToCart(product) {
        emit('add-to-cart', product)
    }

    const removeBankNameList = ['주식회사', '뱅크', '저축', '은행'];

const cleanedName = function(product) {
  let name = product.kor_co_nm;
  if (name.includes('저축')) {
    return '저축';
  }
  if (name.includes('아이엠')) {
    return '대구';
  }
  if (name.includes('한국스탠다드차타드')) {
    return '제일';
  }
  removeBankNameList.forEach(str => {
    const regex = new RegExp(str, 'g');
    name = name.replace(regex, '');
  });
  return name.trim();
};
function bankimg(product) {
  const rrname = cleanedName(product)
  return new URL(`/src/assets/banklogo/${rrname}.png`, import.meta.url).href
}


    onMounted(() => {
        recommendStore.get_recommendByPrivate()
        recommendStore.get_recommendByPrivateForSaving()
    })
</script>




<style scoped>
    h1 {
    margin-bottom: 1rem;
}

.product-card {
    border: 1px solid #ddd;
    padding: 0.5rem;
    border-radius: 8px;
    text-align: center;
    background-color: #fafafa;
    height:250px;
    width: 280px;
}

.swiper-button-prev,
.swiper-button-next {
    color: #000; /* 화살표 색깔 */
    width: 2rem;
    height: 2rem;
}

#ageBox {
    width: 80%;
    margin-top: 30px;
}
.profile-preview {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  /* border: 2px solid #ddd; */
   /* 테두리 추가 */
  margin: 0 auto;
}

.title {
    font-size: 24px;
}

.product-card span {
  color: #666;
}
</style>