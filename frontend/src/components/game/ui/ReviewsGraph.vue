<script setup lang="ts">
import {onMounted, ref, useTemplateRef} from "vue";
import {BackendApiService} from "@/api/backend.ts";
import {useRouter} from "vue-router";

const router = useRouter();

const props = defineProps<{
  ratings: number[],
  game_id: string,
  userRating: number | null,
}>()

const emit = defineEmits(["update-ratings"]);

const ratingsCanvas = useTemplateRef<HTMLCanvasElement>("ratings-canvas");
const ctx = ref();
const hoveredIndex = ref(-1);
const isHovered = ref(false)

const api = new BackendApiService();
if (localStorage.getItem('access_token'))
  api.setToken(localStorage.getItem('access_token') || '');

const reviewRadius = 4,
    workHeight = 50,
    gap = 15;

function getColor(rating: number) {
  if (rating < 3) return "red";
  if (rating < 5) return "orange";
  return "green";
}

function draw(rating = props.ratings) {
  if (!ratingsCanvas.value || !ctx.value) return;
  const canvas = ratingsCanvas.value;
  
  ctx.value.clearRect(0, 0, canvas.width, canvas.height);
  
  ctx.value.fillStyle = "white";
  ctx.value.strokeStyle = "white";
  ctx.value.font = "10px Arial";
  ctx.value.textAlign = "center";
  
  const mostRates = Math.max(...rating);
  
  let lastX, lastY;
  
  rating.forEach((rate, i) => {
    ctx.value.strokeStyle = getColor(i-1);
    ctx.value.beginPath();
    
    const normalizedHeight = (rate / mostRates) * workHeight || 0;
    const padding = (90 - workHeight) / 2;
    const y = padding + (workHeight - normalizedHeight) ;
    const x = i * gap + 6;

    ctx.value.moveTo(lastX, lastY);
    ctx.value.lineTo(x, y);
    
    lastX = x;
    lastY = y;
    
    ctx.value.stroke();
  })

  
  rating.forEach((rate, i) => {
    const normalizedHeight = (rate / mostRates) * workHeight || 0;
    const padding = (90 - workHeight) / 2;
    const y = padding + (workHeight - normalizedHeight) ;
    const x = i * gap + 6;

    ctx.value.fillStyle = getColor(i); 
    ctx.value.beginPath();
    ctx.value.arc(x, y, reviewRadius, 0, Math.PI * 2);
    ctx.value.fill();
    ctx.value.closePath();

    ctx.value.fillStyle = "white";
    ctx.value.fillText(i+1, x, padding * 2 + workHeight - 5);
    
    if (hoveredIndex.value === i)
      ctx.value.fillText((rate).toShortString(), x, 11);
  })
}

function mousemove(ev: MouseEvent) {
  if (!ratingsCanvas.value) return;
  const rect = ratingsCanvas.value.getBoundingClientRect();
  const mouseX = ev.clientX - rect.left;

  let found = false;
  props.ratings.forEach((_, i) => {
    const x = i * gap + 6;
    if (Math.abs(mouseX - x) < 7) {
      hoveredIndex.value = i;
      found = true;
    }
  });
  
  draw(props.ratings.map((v, i) => {
    if (i === hoveredIndex.value && hoveredIndex.value != props.userRating-1) return v+1;
    else if (i == props.userRating-1 && i !== hoveredIndex.value) return v-1;
    else return v;
  }))
}

async function onClick() {
  if (localStorage.getItem('access_token')) {
    const res = await api.rateGame(props.game_id, hoveredIndex.value+1);

    if (res.message == "Rating updated") {
      emit("update-ratings", hoveredIndex.value);
      draw()
    }
  } else {
    await router.push('/login?redirect=' + router.currentRoute.value.fullPath)
  }
}

onMounted(() => {
  ctx.value = ratingsCanvas.value!.getContext("2d");
  
  draw();
})

</script>

<template>
  <div>
    <canvas @click="onClick" @mousemove="mousemove" @mouseenter="isHovered = true" @mouseleave="isHovered = false; hoveredIndex = -1; draw()" ref="ratings-canvas" height="90" width="160"></canvas>
  </div>
</template>

<style scoped>
  div {
    height: 100%;
  }
  canvas {
    cursor: pointer;
  }
</style>