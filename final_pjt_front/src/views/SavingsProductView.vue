<!-- SavingsProductView.vue -->
<template>
    <div class="container">
      <h1 class="title">적금 상품 목록</h1>

      <!-- 은행 선택 Select Box와 버튼을 한 줄로 배치 -->
    <div class="filter-controls">
      <select @change="filterByBank" v-model="selectedBank">
        <option value="">은행을 선택하세요</option>
        <option v-for="bank in bankOptions" :key="bank" :value="bank">
          {{ bank }}
        </option>
      </select>
      <button @click="toggleSortOrder" class="sort-button">
        최고 우대 금리
        <span v-if="sortOrder === 'asc'">▲</span>
        <span v-else>▼</span>
      </button>
    </div>

      <table class="table table-striped">
        <thead class="table-header">
          <tr>
            <th style="width: 10%;">No</th>
            <th style="width: 30%;">상품명</th>
            <th style="width: 20%;">해당은행</th>
            <th style="width: 25%;">가입대상</th>
            <th style="width: 15%;">최고우대금리</th>
            
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(product, index) in paginatedProducts"
            :key="index"
            :class="{ 'odd-row': index % 2 === 0 }"
          >
          <td>{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>
            <td @click="showProductDetail(product)" class="product-name">
              {{ product.fin_prdt_nm }}
            </td>
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.join_member }}</td>
            <td>
              <span v-if="product.highestRateOption.intr_rate2 !== '데이터 없음'">
                {{ product.highestRateOption.intr_rate2 }}%
                ({{ product.highestRateOption.save_trm }}개월)
              </span>
              <span v-else>
                데이터 없음
              </span>
            </td>
          </tr>
        </tbody>
      </table>
  
      <nav>
      <ul class="pagination">
        <li
          class="page-item"
          :class="{ disabled: currentPage === 1 }"
          @click="changePage(currentPage - 1)"
        >
          <a class="page-link">‹</a>
        </li>
        <li
          v-for="page in visiblePages"
          :key="page"
          class="page-item"
          :class="{ active: currentPage === page }"
          @click="changePage(page)"
        >
          <a class="page-link">{{ page }}</a>
        </li>
        <li
          class="page-item"
          :class="{ disabled: currentPage === totalPages }"
          @click="changePage(currentPage + 1)"
        >
          <a class="page-link">›</a>
        </li>
      </ul>
    </nav>
  
      <!-- ProductDetailCard 컴포넌트를 조건부 렌더링 -->
      <SavingProductDetail
        v-if="selectedProduct"
        :product="selectedProduct"
        @close="selectedProduct = null"
      />
    </div>
  </template>
  
  <script>
  import { useSavingStore } from "@/stores/saving";
  import { onMounted, computed, ref } from "vue";
  import SavingProductDetail from "@/components/SavingProductDetail.vue";
  
  export default {
    components : { SavingProductDetail },
    setup() {
      const savingStore = useSavingStore();
      const currentPage = ref(1);
      const itemsPerPage = 10;
      const selectedProduct = ref(null)
      const selectedBank = ref("");
      const bankOptions = ref([]);
      const sortOrder = ref("asc");
  
      onMounted(async () => {
        await savingStore.getSavingProductsWithHighestRate();
        bankOptions.value = [
        ...new Set(savingStore.savingProductsData.map((p) => p.kor_co_nm)),
      ];
      });
  
      
      const filteredProducts = computed(() => {
        let products = savingStore.savingProductsData;
        
        if (selectedBank.value) {
          products = products.filter(
            (product) => product.kor_co_nm === selectedBank.value
          );
        }
        
        products = products.slice().sort((a, b) => {
          const rateA = a.highestRateOption.intr_rate2 || 0;
          const rateB = b.highestRateOption.intr_rate2 || 0;
          return sortOrder.value === "asc" ? rateA - rateB : rateB - rateA;
        });
        
        return products;
      });
      
      const totalPages = computed(() => {
        return Math.ceil(filteredProducts.value.length / itemsPerPage);
      });

      const visiblePages = computed(() => {
      const pages = [];
      const startPage = Math.floor((currentPage.value - 1) / 10) * 10 + 1;
      const endPage = Math.min(startPage + 9, totalPages.value);

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }

      return pages;
    });

      const paginatedProducts = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return filteredProducts.value.slice(start, end);
      });
  
      const changePage = (page) => {
        if (page > 0 && page <= totalPages.value) {
          currentPage.value = page;
        }
      };

    const filterByBank = () => {
      currentPage.value = 1;
    };

    const toggleSortOrder = () => {
      sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
      currentPage.value = 1;
    };
  
      const showProductDetail = (product) => {
        selectedProduct.value = product;
      };
  
      return {
        savingStore,
        currentPage,
        itemsPerPage,
        paginatedProducts,
        totalPages,
        changePage,
        selectedProduct,
        showProductDetail,
        selectedBank,
        bankOptions,
        filteredProducts,
        filterByBank,
        sortOrder,
        toggleSortOrder,
        visiblePages
      };
    },
  };
  </script>
  
  <style scoped>
/* 기본 컨테이너 설정 */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* 현대적인 서체 */
  padding: 20px;
  background-color: #fafafa; /* 연한 회색 배경 */
  max-width: 1100px;
}

/* 테이블 헤더 */
.table-header {
  background-color: #f1f1f1; /* 부드러운 그라데이션 느낌 */
  color: #333; /* 진한 텍스트 */
}

/* 테이블 기본 스타일 */
.table {
  margin-top: 20px;
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 미세한 그림자 효과 */
  border-radius: 10px; /* 테이블의 모서리 둥글게 */
  overflow: hidden; /* 테이블 경계의 깔끔한 모서리 */
}

.table th,
.table td {
  text-align: center;
  vertical-align: middle;
  padding: 12px 15px;
  font-size: 14px; /* 폰트 크기 조금 더 작게 */
  border-bottom: 1px solid #e1e1e1; /* 얇은 회색 구분선 */
}

.odd-row {
  background-color: #f9f9f9; /* 아주 연한 회색으로 홀수 행 구분 */
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 10px; /* 페이지 버튼 사이 간격 */
}

.pagination .page-item a.page-link {
    color: #b19cd9;
    background: none;
    border: none;
    cursor: pointer;
    margin: 0 5px;
  }
  
  .pagination .page-item a.page-link:hover {
    color: #6f42c1;
  }
  
  .pagination .page-item.active a.page-link {
    color: #6f42c1;
    font-weight: bold;
  }

/* 상품명 스타일링 */
.product-name {
  color: #333; /* 기본 텍스트 색상 */
  cursor: pointer;
  font-weight: 600; /* 굵은 텍스트 */
  text-decoration: underline; /* 밑줄 효과 */
  transition: color 0.3s ease, text-decoration 0.3s ease;
}

.product-name:hover {
  color: #6a4cfa; /* 보라색으로 변환 */
  text-decoration: none; /* 밑줄 제거 */
}

.filter-controls {
  display: flex;
  align-items: center; /* 아이템을 세로로 정렬 */
  gap: 10px; /* 간격 조정 */
  margin-bottom: 20px; /* 아래 콘텐츠와 간격 */
  justify-content: flex-start; /* 왼쪽 정렬 */
}

select {
  padding: 10px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 10px; /* 둥근 버튼 스타일 */
  background-color: #fff;
  transition: all 0.3s ease;
}

select:hover {
  border-color: #6a4cfa; /* hover 시 보라색 테두리 */
}

.sort-button {
  display: flex; /* flex로 버튼 내 요소 정렬 */
  align-items: center; /* 화살표와 텍스트를 세로로 정렬 */
  gap: 5px; /* 글씨와 화살표 사이 간격 */
  padding: 5px 10px; /* 버튼 안쪽 여백 */
  font-size: 16px;
  background-color: #6f42c1; /* 보라색 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 150px;
}

.pagination .page-item a.page-link:hover {
  background-color: #f1f1f1; /* 마우스 올렸을 때 배경 색상 */
}

/* 텍스트 제한 */
.limited-text {
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 3줄까지만 표시 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #666; /* 연한 회색 */
}

/* 모바일 스타일 */
@media (max-width: 768px) {
  .filter-controls {
    flex-direction: column;
    align-items: flex-start;
  }

  select, .sort-button {
    width: 100%; /* 모바일에서 입력창 및 버튼 가로 너비 100% */
  }

  .pagination .page-item a.page-link {
    padding: 6px 8px;
  }
}

.title {
  font-family: 'Godo', sans-serif;
  font-weight: bold;
}

@font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'),
      url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}
</style>