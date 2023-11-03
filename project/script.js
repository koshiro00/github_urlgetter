/* ■■■■■■■■■■■■■■■■■■■■■■ */
/* ↓ genneral functions ↓ */
/* ■■■■■■■■■■■■■■■■■■■■■■ */

const mainContents = document.getElementById("wrapper")
const loading = document.getElementById("loading");

const switchElem = (hiddenElem, onElem) => {
  hiddenElem.style.display = "none";
  if(onElem){
    onElem.style.display = "block";
  }
}


/* ■■■■■■■■■■■■■■■■■■ */
/* ↓     action    ↓  */
/* ■■■■■■■■■■■■■■■■■■ */

window.addEventListener('pywebviewready', async () => {
  await loadRepositories();
  switchElem(loading, mainContents);
});

document.querySelector(".update").addEventListener("click", async () => {
  switchElem(mainContents, loading);
  await loadRepositories();
  switchElem(loading, mainContents);
});

document.getElementById("submitBtn").addEventListener("click", () => {
  switchElem(mainContents, loading)
  onSubmit();
});

/* ■■■■■■■■■■■■■■■■■■ */
/* ↓ main functions ↓ */
/* ■■■■■■■■■■■■■■■■■■ */

async function loadRepositories() {
  try {
    const content = document.querySelector(".container");
    while(content.firstChild){
      content.removeChild(content.firstChild);
    }
    const repos = await window.pywebview.api.get_repositories();
    for (let i = 0; i < repos.length; i++) {
      await displayRepositoryInfo(repos[i], i + 1);
    }
    addSelectedClass();
  } catch (error) {
    console.log("loadRepositories ", error);
  }
}

let selectedBox = null;  // 選択されたboxの監視用
function addSelectedClass(){
  const selectBoxes = document.querySelectorAll(".select_box");
  selectBoxes.forEach((box) => {
    box.addEventListener("click", () => {
      if(selectedBox) {
        selectedBox.classList.remove("selected");  // 前に選択された要素からクラスを削除
      }
      box.classList.add("selected");  // 新しく選択された要素にクラスを追加
      selectedBox = box;  // 選択された要素を更新
    });
  });
}

async function onSubmit(){
  try {
    const targetElem = document.querySelector(".selected .repository p:nth-child(1)");
    const repo = targetElem.textContent;
    // このデータをPythonに送信
    await window.pywebview.api.submit({repo});
    window.alert("完了しました")
  } catch (error) {
    console.log("onSubmit ", error)
  }
}

/* ■■■■■■■■■■■■■■■■■■ */
/* ↓ sub functions ↓ */
/* ■■■■■■■■■■■■■■■■■■ */

async function displayRepositoryInfo(repoName, count) {
  try {
    const repoInfo = await window.pywebview.api.get_repository_info(repoName);
    const container = document.querySelector('.container');

    // Create elements based on the provided HTML structure
    const selectBox = elemGeneration('div', 'select_box', container);
    const flexDiv = elemGeneration('div', 'flex', selectBox);
    const numberIconDiv = elemGeneration('div', 'number_icon', flexDiv);
    const numberIconImg = elemGeneration('img', '', numberIconDiv);
    numberIconImg.src = `https://img.icons8.com/ios/50/${count}-circle.png`;
    numberIconImg.alt = "1-circle";
    
    const repositoryDiv = elemGeneration('div', 'repository', flexDiv);

    repositoryDiv.innerHTML = `
      <p>${repoInfo.name}</p>
      <p>${repoInfo.lastCommitDate} / ${repoInfo.isPublic ? 'public' : 'private'}</p>
    `;

    const gitIconDiv = elemGeneration('div', 'git_icon', selectBox);
    const gitIconImg = elemGeneration('img', '', gitIconDiv);
    gitIconImg.src = "https://img.icons8.com/ios/50/000000/github--v1.png";
    gitIconImg.alt = "github--v1";

  } catch (error) {
    console.log("displayRepositoryInfo error: ", error);
  }
}
// Element generation helper function
const elemGeneration = (elemType, className, parentElem, innerElem) => {
  if (!elemType) {
    console.error("Invalid element type:", elemType);
    return null;
  }
  const elem = document.createElement(elemType);
  if (className) {
    elem.classList.add(className);
  }
  if (parentElem) {
    parentElem.appendChild(elem);
  }
  if (innerElem) {
    elem.appendChild(innerElem);
  }
  return elem;
};
