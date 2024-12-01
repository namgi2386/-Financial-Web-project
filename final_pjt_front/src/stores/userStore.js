import { ref, computed, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";
import { useRouter } from 'vue-router';
import swal from 'sweetalert';

export const useUserStore = defineStore('user', () => {
    const BASE_URL = 'http://localhost:8000/accounts'
    const token = ref(null)
    const router = useRouter()
    const likedProducts = ref([]); // 사용자가 좋아요를 누른 상품 목록
    
    // 좋아요 추가
    const addLikedProduct = (productCode) => {
        if (!likedProducts.value.includes(productCode)) {
        likedProducts.value.push(productCode);
        }
    };

    // 좋아요 취소 (삭제)
    const removeLikedProduct = (productCode) => {
        const index = likedProducts.value.indexOf(productCode);
        if (index !== -1) {
        likedProducts.value.splice(index, 1);
        }
    };

    // 좋아요 여부 확인
    const isLiked = (productCode) => {
        return likedProducts.value.includes(productCode);
    };

    
    const isLogin = computed(() => {
        if (token.value === null) {
            return false
        } else {
            return true
        }
    })


    const signUp = function(payload) {
        const { username, password1, password2, age, money , nickname , desiredSubscriptionPeriod , mainBank} = payload
        console.log(payload);
        
        axios({
            url: `${BASE_URL}/signup/`,
            method: 'POST',
            data: {
                username,
                password1,
                password2,
                age,
                money,
                nickname,
                desiredSubscriptionPeriod,
                mainBank,
            },
            
        }).then(response => {
            console.log(response);
            logIn({ username, password: password1 });
        }).catch(error => {
            console.log(error);
            swal({
                icon: 'error',
                title: '중복된 아이디입니다!',
                // text: '회원가입 요청이 정상적으로 처리되었습니다.',
              });
        });
    }

    const logIn = (payload) => {
        axios({
            url: `${BASE_URL}/login/`,
            method: 'POST',
            data: {
                username: payload.username,
                password: payload.password
            }
        }).then(response => {
            console.log(response);
            token.value = response.data.key;
            localStorage.setItem('token', token.value); // 로컬 스토리지에 토큰 저장
            console.log(token.value)
            localStorage.setItem('locusername', payload.username);
            router.push({name: 'profile'})
        }).then(()=> {
            setDBDeposit()
        }).then(()=> {
            setDBSaving()
        })
        .catch(error => {
            // 에러 응답 처리
            if (error.response) {
                if (error.response.status === 404) {
                    alert("아이디가 존재하지 않습니다."); // 404: 아이디가 없음
                } else if (error.response.status === 401) {
                    alert("아이디와 비밀번호를 확인해주세요."); // 401: 인증 실패
                } else {
                    swal({
                        icon: 'error',
                        title: '로그인 실패',
                        text: '아이디 혹은 비밀번호를 확인하세요.',
                      });
                }
            } else {
                console.error("서버에 연결할 수 없습니다.");
                alert("서버에 문제가 발생했습니다. 나중에 다시 시도해주세요.");
            }
        });
    };

    const logOut = function() {
        axios({
            method: 'post',
            url: `${BASE_URL}/logout/`,
        })
            .then((res) => {
                console.log(res)
                // 로그아웃 이후 해야하는 것들
                localStorage.removeItem('token'); // 로컬 스토리지에서 토큰 제거
                localStorage.removeItem('locusername'); // 로컬 스토리지에서 토큰 제거
                token.value= null
                router.push({name: "main"})
            })
            .catch((err) => {
                console.log(err)
            })
    }

    const profileData = ref([])
    const getProfile = function() {
        const token = localStorage.getItem('token');
        axios({
            method: "GET",
            url : `${BASE_URL}/profile`,
            headers: {Authorization: `Token ${token}`},
        })
        .then( (res)=> {
            console.log(res.data);
            profileData.value = res.data
        })
        .catch((err) => {
            console.log(err)
        })
    }
    const finInfoData = ref([])
    const getFinInfo = function() {
        const token = localStorage.getItem('token');
        axios({
            method: "GET",
            url : `${BASE_URL}/fininfo`,
            headers: {Authorization: `Token ${token}`},
        })
        .then( (res)=> {
            console.log(res.data);
            finInfoData.value = res.data
        })
        .catch((err) => {
            console.log(err)
        })
    }

    const setDBDeposit = function () {
        const BASE_URL_FIN = "http://localhost:8000/finlife"
        const token = localStorage.getItem('token');
        axios({
        method: "get",
        url: `${BASE_URL_FIN}/save-deposit-products/`,
        headers: {
            Authorization: `Token ${token}`,
        },
        })
        .then((res) => {
            console.log("save deposit");
        })
        .catch((err) => {
            console.log("saving error");
            
            console.log(err);
        });
    };
    // 처음에 DB에 저장하는 함수
    const setDBSaving = function () {
        const BASE_URL_FIN = "http://localhost:8000/finlife"
        const token = localStorage.getItem('token');
        axios({
        method: "get",
        url: `${BASE_URL_FIN}/save-saving-products/`,
        headers: {
            Authorization: `Token ${token}`,
        },
        })
        .then((res) => {
            console.log("save saving");
        })
        .catch((err) => {
            console.log("saving error");
            
            console.log(err);
        });
    };

    const profileDetailData = ref([])
    const getProfileDetail = function(num) {
        const token = localStorage.getItem('token');
        axios({
            method: "GET",
            url : `${BASE_URL}/profile/${num}/`,
            headers: {Authorization: `Token ${token}`},
        })
        .then( (res)=> {
            console.log(res.data);
            profileDetailData.value.push(res.data       )     
            // profileDetailData.value.pop
            console.log(profileDetailData.value);
            
        })
        .catch((err) => {
            console.log(err)
        })
    }

    onMounted(() => {
        // 앱이 시작될 때 로컬 스토리지에서 토큰을 확인
        const savedToken = localStorage.getItem('token');
        if (savedToken) {
            token.value = savedToken; // 로컬 스토리지에 있는 토큰을 token에 할당
        }
    });

    return {
        BASE_URL,
        token,
        signUp,
        logIn,
        logOut,
        router,
        isLogin,
        getProfile,
        profileData,
        getFinInfo,
        finInfoData,
        setDBDeposit,
        setDBSaving,
        addLikedProduct,
        removeLikedProduct,
        isLiked,
        likedProducts , getProfileDetail , profileDetailData
    }
}, { persist: true })
