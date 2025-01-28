<template>
  <footer class="footer-container">
    <div class="info">
      <img src="/images/info_white.png" alt="info" />
    </div>
    <div class="holberton">
      <a href="https://www.holbertonschool.fr/" target="_blank">
        <img src="/images/seahorse_white.png" alt="holberton" />
      </a>
    </div>
    <div class="github">
        <a href="https://github.com/MgCodeFactory/planner_outdoor" target="_blank">
          <img src="/images/github.png" alt="github project" />
        </a>
    </div>
    <div class="linkedin">
        <a href="https://www.linkedin.com/in/emmanuel-mg197274470/" target="_blank">
          <img src="/images/linkedin.png" alt="linkedin" />
        </a>
    </div>
  </footer>
</template>

<script>
export default {
  name: "PageFooter",
};
</script>

<style scoped>
.footer-container {
  order: 2; /* item of app-container*/
  display: flex;
  flex-direction: row;
  flex-grow: 0;
  justify-content: center;
  align-items: center;
  gap: 0;
  height: var(--header-footer-height);
  background-color: var(--color-header-footer);
  color: var(--color-white);
}

.info {
  order: 0; /* item of footer-container*/
  display: flex;
  justify-content: center;
  align-items: center;
}

.holberton {
  order: 1; /* item of footer-container*/
  display: flex;
  justify-content: center;
  align-items: center;
}

.github {
  order: 2; /* item of footer-container*/
  display: flex;
  justify-content: center;
  align-items: center;
}

.linkedin {
  order: 3; /* item of footer-container*/
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-container > div img {
  height: 30px;
  width: 30px;
}

.footer-container > div {
  flex-grow: 0;
  width: 3vw;
  height: 100%;
}

.footer-container > div img:hover {
  height: 40px;
  width: 40px;
  cursor: pointer;
}
</style>
