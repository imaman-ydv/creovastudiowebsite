import * as THREE from "./vendor/three/three.module.js";

const stage = document.querySelector(".hero-art");
const canvas = stage?.querySelector(".hero-canvas");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (stage && canvas) {
  try {
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: "low-power" });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 40);
    camera.position.set(0, 0.05, 7.6);

    scene.add(new THREE.HemisphereLight(0xf8f5ed, 0x34343a, 2.2));
    const keyLight = new THREE.DirectionalLight(0xffffff, 3.2);
    keyLight.position.set(-3.5, 4.5, 5);
    scene.add(keyLight);
    const rimLight = new THREE.PointLight(0xff6542, 22, 8, 2);
    rimLight.position.set(2.2, 0.2, 2.8);
    scene.add(rimLight);

    const sculpture = new THREE.Group();
    scene.add(sculpture);

    const porcelain = new THREE.MeshPhysicalMaterial({ color: 0xf1ede4, roughness: 0.16, metalness: 0.62, clearcoat: 1, clearcoatRoughness: 0.08 });
    const shadow = new THREE.MeshPhysicalMaterial({ color: 0x77777e, roughness: 0.24, metalness: 0.72, clearcoat: 0.8 });
    const dark = new THREE.MeshPhysicalMaterial({ color: 0x171715, roughness: 0.2, metalness: 0.76, clearcoat: 1 });
    const signal = new THREE.MeshPhysicalMaterial({ color: 0xff6542, emissive: 0xff351b, emissiveIntensity: 0.8, roughness: 0.13, metalness: 0.32, clearcoat: 1 });
    const glass = new THREE.MeshPhysicalMaterial({ color: 0xff8b70, roughness: 0.09, metalness: 0.08, transmission: 0.58, thickness: 0.65, clearcoat: 1, clearcoatRoughness: 0.04, transparent: true, opacity: 0.94 });

    const addMesh = (geometry, material, parent, position, scale, rotation = [0, 0, 0]) => {
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.set(...position);
      mesh.scale.set(...scale);
      mesh.rotation.set(...rotation);
      parent.add(mesh);
      return mesh;
    };

    // A friendly original robot built from soft 3D forms and glassy orange details.
    const robotWhite = new THREE.MeshPhysicalMaterial({ color: 0xf3f0e9, roughness: 0.2, metalness: 0.28, clearcoat: 0.92, clearcoatRoughness: 0.12 });
    const robotDark = new THREE.MeshPhysicalMaterial({ color: 0x242426, roughness: 0.22, metalness: 0.35, clearcoat: 0.85 });
    const warmGlass = new THREE.MeshPhysicalMaterial({ color: 0xff886f, roughness: 0.08, metalness: 0.05, transmission: 0.45, thickness: 0.55, clearcoat: 1, clearcoatRoughness: 0.04, transparent: true, opacity: 0.9 });

    // Rounded head shell, ear caps, and antenna.
    addMesh(new THREE.SphereGeometry(1, 48, 32), robotWhite, sculpture, [0, 0.43, 0], [1.02, 0.93, 0.72]);
    addMesh(new THREE.SphereGeometry(0.17, 24, 16), signal, sculpture, [-1.055, 0.4, 0.01], [1, 1, 0.55]);
    addMesh(new THREE.SphereGeometry(0.17, 24, 16), signal, sculpture, [1.055, 0.4, 0.01], [1, 1, 0.55]);
    addMesh(new THREE.CylinderGeometry(0.035, 0.05, 0.27, 16), shadow, sculpture, [0, 1.32, 0], [1, 1, 1], [0, 0, -0.08]);
    addMesh(new THREE.SphereGeometry(0.12, 24, 16), signal, sculpture, [-0.02, 1.49, 0], [1, 1, 1]);
    addMesh(new THREE.TorusGeometry(0.12, 0.035, 10, 32), warmGlass, sculpture, [-0.02, 1.49, 0.02], [1, 1, 1]);

    // Big kind eyes with dark cushions, bright amber irises, and tiny catchlights.
    [-0.39, 0.39].forEach((x) => {
      addMesh(new THREE.SphereGeometry(0.235, 32, 24), robotDark, sculpture, [x, 0.42, 0.635], [1, 1.04, 0.42]);
      addMesh(new THREE.SphereGeometry(0.147, 32, 24), signal, sculpture, [x, 0.43, 0.73], [0.9, 1.04, 0.52]);
      addMesh(new THREE.SphereGeometry(0.038, 16, 12), robotWhite, sculpture, [x - 0.035, 0.49, 0.8], [1, 1, 0.5]);
    });
    const leftCheek = addMesh(new THREE.SphereGeometry(0.09, 20, 14), warmGlass, sculpture, [-0.68, 0.08, 0.61], [1.25, 0.55, 0.4]);
    const rightCheek = addMesh(new THREE.SphereGeometry(0.09, 20, 14), warmGlass, sculpture, [0.68, 0.08, 0.61], [1.25, 0.55, 0.4]);
    const smile = new THREE.QuadraticBezierCurve3(new THREE.Vector3(-0.23, 0.06, 0.68), new THREE.Vector3(0, -0.12, 0.77), new THREE.Vector3(0.23, 0.06, 0.68));
    const smileMesh = addMesh(new THREE.TubeGeometry(smile, 28, 0.026, 8, false), robotDark, sculpture, [0, 0, 0], [1, 1, 1]);

    // Neck and compact body with a small glass control panel.
    addMesh(new THREE.CylinderGeometry(0.23, 0.28, 0.42, 32), shadow, sculpture, [0, -0.68, 0], [1, 1, 1]);
    addMesh(new THREE.SphereGeometry(0.83, 40, 28), robotWhite, sculpture, [0, -1.28, 0], [1.18, 0.68, 0.72]);
    const makeArm = (side) => {
      const arm = new THREE.Group();
      arm.position.set(side * 0.88, -1.02, 0.04);
      sculpture.add(arm);
      addMesh(new THREE.CapsuleGeometry(0.12, 0.38, 6, 16), robotWhite, arm, [side * 0.1, -0.28, 0.03], [1, 1, 1], [0, 0, -side * 0.2]);
      addMesh(new THREE.SphereGeometry(0.15, 24, 16), warmGlass, arm, [side * 0.18, -0.57, 0.11], [1, 1, 0.72]);
      return arm;
    };
    const leftArm = makeArm(-1);
    const rightArm = makeArm(1);
    addMesh(new THREE.BoxGeometry(0.74, 0.32, 0.075), robotDark, sculpture, [0, -1.3, 0.62], [1, 1, 1]);
    addMesh(new THREE.BoxGeometry(0.43, 0.045, 0.035), signal, sculpture, [0, -1.31, 0.67], [1, 1, 1]);
    [-0.24, 0.24].forEach((x) => addMesh(new THREE.SphereGeometry(0.045, 16, 12), warmGlass, sculpture, [x, -1.18, 0.68], [1, 1, 0.45]));
    addMesh(new THREE.IcosahedronGeometry(0.14, 0), shadow, sculpture, [-1.45, 0.83, -0.1], [1, 1, 1], [0.3, 0.4, 0.1]);
    addMesh(new THREE.IcosahedronGeometry(0.1, 0), signal, sculpture, [1.42, -0.82, 0.1], [1, 1, 1], [0.2, 0.1, 0.4]);

    const orbitMaterial = new THREE.MeshBasicMaterial({ color: 0xff6542, transparent: true, opacity: 0.86 });
    const paleOrbitMaterial = new THREE.MeshBasicMaterial({ color: 0xf8f5ed, transparent: true, opacity: 0.45 });
    const orbit = new THREE.Group();
    scene.add(orbit);
    const orbitOne = new THREE.Mesh(new THREE.TorusGeometry(1.95, 0.009, 5, 150), orbitMaterial);
    orbitOne.rotation.set(1.18, 0.14, -0.3);
    orbit.add(orbitOne);
    const orbitTwo = new THREE.Mesh(new THREE.TorusGeometry(1.72, 0.006, 5, 150), paleOrbitMaterial);
    orbitTwo.rotation.set(1.34, -0.36, 0.28);
    orbit.add(orbitTwo);
    addMesh(new THREE.SphereGeometry(0.055, 12, 8), signal, orbit, [1.48, 0.78, 0.05], [1, 1, 1]);

    const pointer = { x: 0, y: 0 };
    const target = { x: 0, y: 0 };
    const gesture = { amount: 0 };
    let celebrationUntil = 0;
    let celebrationTimer;
    let friendlyMood = false;
    const appreciationNote = stage.querySelector(".appreciation-note");
    const applyGesture = (amount, time = 0) => {
      leftArm.rotation.z = -amount * 2.2;
      rightArm.rotation.z = amount * (2.25 + Math.sin(time * 9) * 0.18);
      smileMesh.scale.set(1 + amount * 0.46, 1 + amount * 0.12, 1);
      leftCheek.scale.set(1.25 + amount * 0.35, 0.55 + amount * 0.18, 0.4);
      rightCheek.scale.set(1.25 + amount * 0.35, 0.55 + amount * 0.18, 0.4);
    };
    const contactLink = document.querySelector(".nav-contact");
    const robotRequest = document.querySelector(".robot-please");
    const setFriendlyMood = (active) => {
      friendlyMood = active;
      if (reduceMotion && performance.now() >= celebrationUntil) {
        applyGesture(active ? 0.48 : 0);
        renderer.render(scene, camera);
      }
    };
    const celebrate = () => {
      celebrationUntil = performance.now() + 2600;
      stage.removeAttribute("data-celebrating");
      void stage.offsetWidth;
      stage.dataset.celebrating = "true";
      appreciationNote?.setAttribute("aria-hidden", "false");
      clearTimeout(celebrationTimer);
      celebrationTimer = setTimeout(() => {
        if (performance.now() < celebrationUntil) return;
        delete stage.dataset.celebrating;
        appreciationNote?.setAttribute("aria-hidden", "true");
        if (reduceMotion) {
          applyGesture(friendlyMood ? 0.48 : 0);
          renderer.render(scene, camera);
        }
      }, 2650);
      if (reduceMotion) {
        applyGesture(1);
        renderer.render(scene, camera);
      }
    };
    [contactLink, robotRequest].forEach((control) => {
      control?.addEventListener("pointerenter", () => setFriendlyMood(true));
      control?.addEventListener("pointerleave", () => setFriendlyMood(false));
      control?.addEventListener("focus", () => setFriendlyMood(true));
      control?.addEventListener("blur", () => setFriendlyMood(false));
    });
    robotRequest?.addEventListener("click", celebrate);

    if (window.matchMedia("(pointer: fine)").matches) {
      const updatePointer = (event) => {
        target.x = (event.clientX / window.innerWidth - 0.5) * 0.9;
        target.y = (event.clientY / window.innerHeight - 0.5) * 0.7;
        if (reduceMotion) {
          sculpture.rotation.y = target.x;
          sculpture.rotation.x = target.y;
          sculpture.position.x = target.x * 0.72;
          sculpture.position.y = -target.y * 0.32;
          renderer.render(scene, camera);
        }
      };
      const resetPointer = () => {
        target.x = 0;
        target.y = 0;
        if (reduceMotion) {
          sculpture.rotation.set(0, 0, 0);
          sculpture.position.set(0, 0, 0);
          renderer.render(scene, camera);
        }
      };
      window.addEventListener("pointermove", updatePointer, { passive: true });
      window.addEventListener("blur", resetPointer);
    }

    const resize = () => {
      const width = stage.clientWidth;
      const height = stage.clientHeight;
      if (!width || !height) return;
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.position.z = width < 520 ? 8.1 : 7.6;
      camera.updateProjectionMatrix();
      renderer.render(scene, camera);
    };
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(stage);
    resize();
    stage.dataset.webglReady = "true";

    if (!reduceMotion) {
      const clock = new THREE.Clock();
      const animate = () => {
        const time = clock.getElapsedTime();
        pointer.x += (target.x - pointer.x) * 0.075;
        pointer.y += (target.y - pointer.y) * 0.075;
        const celebrating = performance.now() < celebrationUntil;
        const gestureTarget = celebrating ? 1 : friendlyMood ? 0.48 : 0;
        gesture.amount += (gestureTarget - gesture.amount) * 0.12;
        applyGesture(gesture.amount, time);
        sculpture.rotation.y = Math.sin(time * 0.34) * 0.12 + pointer.x;
        sculpture.rotation.x = Math.sin(time * 0.25) * 0.025 + pointer.y + gesture.amount * 0.045;
        sculpture.position.x = pointer.x * 0.72;
        sculpture.position.y = Math.sin(time * 0.75) * 0.065 - pointer.y * 0.32 + gesture.amount * 0.12;
        orbit.rotation.z = Math.sin(time * 0.18) * 0.045;
        orbit.rotation.y = Math.sin(time * 0.2) * 0.06;
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
      };
      requestAnimationFrame(animate);
    }
  } catch (error) {
    console.warn("3D hero unavailable; showing the lightweight vector fallback.", error);
    stage.dataset.webglReady = "false";
  }
}
