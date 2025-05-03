<template>
  <div>
    <!-- Bouton de navigation principal -->
    <button @click="toggleView" class="nav-button">
      {{ showEnvironments ? 'Retour au questionnaire' : 'Voir les environnements' }}
    </button>

    <div v-if="!showEnvironments" class="questionnaire-container">
      <!-- Conteneur principal centré -->
      <div class="main-panel">
        
        <!-- Titre avec style pastel -->
        <div class="title-container">
          <h1 class="main-title">
            Questionnaire sur la concentration et l'organisation du travail
          </h1>
        </div>
        
        <!-- Contenu du questionnaire (visible uniquement si non terminé) -->
        <div v-if="!termine" class="questionnaire-content">
          <!-- Catégorie actuelle - style pastel -->
          <div class="category-header">
            <h2>{{ categories[currentCategoryIndex] }}</h2>
          </div>
          
          <!-- Barre de progression stylisée -->
          <div class="progress-container">
            <div 
              :style="{ width: pourcentage + '%' }"
              class="progress-bar"
            ></div>
          </div>
          
          <!-- Compteur de questions avec design pastel -->
          <div class="question-counter">
            <div class="question-badge">
              Question {{ currentQuestionNumber }}
            </div>
            <div class="question-total">
              {{ currentQuestionNumber }} sur {{ totalQuestions }}
            </div>
          </div>
          
          <!-- Question avec style pastel -->
          <div class="question-panel">
            <h2>{{ currentQuestion.texte }}</h2>
          </div>
          
          <!-- Options de réponse avec design pastel -->
          <div v-if="currentQuestion.type === 'choix'" class="choices-container">
            <div class="choices-wrapper">
              <button
                v-for="(option, index) in currentQuestion.options"
                :key="index"
                @click="choisir(option.texte, option.valeur)"
                class="choice-button"
              >
                <span class="choice-letter">{{ String.fromCharCode(97 + index) }}</span>
                <span class="choice-text">{{ option.texte }}</span>
              </button>
            </div>
          </div>

          <!-- Question spéciale (réponse ouverte) avec style pastel -->
          <div v-if="currentQuestion.type === 'ouvert'" class="open-response">
            <div class="textarea-container">
              <textarea 
                v-model="reponseOuverte" 
                placeholder="Votre réponse..."
                class="open-textarea"
              ></textarea>
            </div>
            <div class="submit-container">
              <button 
                @click="soumettreReponseOuverte" 
                class="submit-button"
              >
                Soumettre
              </button>
            </div>
          </div>
        </div>
        
        <!-- Écran de fin -->
        <div v-if="termine" class="completion-screen">
          <div class="completion-content">
            <div class="completion-circle">
              <span>✓</span>
            </div>
            <h2 class="completion-title">Résultat</h2>
            
            <div class="concentration-result">
              <p>Votre niveau de concentration est : 
                <span class="concentration-level" :data-level="concentrationLevel">
                  {{ concentrationLevel || 'En cours d\'analyse...' }}
                </span>
              </p>
              
              <p class="completion-text">Nous avons analysé votre profil de concentration.</p>
              <p v-if="scoreDetails">
                Organisation: {{ Math.round(scoreDetails.organisation * 100) }}% | 
                Concentration: {{ Math.round(scoreDetails.concentration * 100) }}% | 
                Motivation: {{ Math.round(scoreDetails.motivation * 100) }}%
              </p>
            </div>
            
            <div class="button-container">
              <button 
                @click="navigateToTimeTable" 
                class="start-study-button"
              >
                Commencer l'étude
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Vue des environnements -->
    <div v-if="showEnvironments" class="environments-view">
      <EmploiUpload 
        :niveau="concentrationLevel"
        ref="emploiUpload"
      />
      <EmploiCree 
  :niveau="concentrationLevel" 
  @enregistrer="handleEnregistrement"
/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import EmploiCree from './EmploiCree.vue'; // Ajustez le chemin selon votre structure

export default {
  components: {
    EmploiCree,
  },
  data() {
    return {
      concentrationLevel: null,
      niveauDetecte: null,
      showEnvironments: false,
      termine: false,
      timetableData: [],
      scoreDetails: null,
      categories: [
        "Organisation des études",
        "Habitudes de travail et concentration",
        "Gestion des pauses et de la motivation",
        "Personnalisation et suggestions"
      ],
      questionsParCategorie: [
        // Catégorie 1: Organisation des études
        [
          {
            texte: "Comment organises-tu ton emploi du temps ?",
            type: "choix",
            options: [
              { texte: "J'ai un planning détaillé et je le respecte", valeur: 3 },
              { texte: "J'ai un planning, mais j'ai du mal à le suivre", valeur: 2 },
              { texte: "Je n'ai pas de planning précis", valeur: 1 }
            ]
          },
          {
            texte: "À quelle fréquence procrastines-tu ?",
            type: "choix",
            options: [
              { texte: "Très rarement, je fais mes tâches immédiatement", valeur: 3 },
              { texte: "Parfois, surtout pour les tâches longues", valeur: 2 },
              { texte: "Souvent, je reporte jusqu'à la dernière minute", valeur: 1 }
            ]
          },
          {
            texte: "Comment gères-tu les distractions en étudiant ?",
            type: "choix",
            options: [
              { texte: "J'éteins mon téléphone et je me coupe des distractions", valeur: 3 },
              { texte: "Je consulte parfois mon téléphone, mais je me reconcentre vite", valeur: 2 },
              { texte: "Je suis souvent distrait(e) et j'ai du mal à revenir à mon travail", valeur: 1 }
            ]
          },
          {
            texte: "As-tu l'habitude de planifier tes objectifs pour la semaine ?",
            type: "choix",
            options: [
              { texte: "Oui, je les note et je les suis", valeur: 3 },
              { texte: "Je les ai en tête sans les noter", valeur: 2 },
              { texte: "Je n'y pense pas vraiment", valeur: 1 }
            ]
          }
        ],
        // Catégorie 2: Habitudes de travail et concentration
        [
          {
            texte: "Combien de temps arrives-tu à rester concentré(e) sans interruption ?",
            type: "choix",
            options: [
              { texte: "Plus de 45 minutes", valeur: 3 },
              { texte: "Entre 20 et 45 minutes", valeur: 2 },
              { texte: "Moins de 20 minutes", valeur: 1 }
            ]
          },
          {
            texte: "Quel environnement de travail préfères-tu ?",
            type: "choix",
            options: [
              { texte: "Un lieu calme et structuré", valeur: 3 },
              { texte: "Un lieu avec du bruit modéré (café, musique en fond)", valeur: 2 },
              { texte: "Peu importe, je travaille n'importe où", valeur: 1 }
            ]
          },
          {
            texte: "Quand tu étudies, quelles sont tes principales distractions ?",
            type: "choix",
            options: [
              { texte: "Aucune, je reste très concentré(e)", valeur: 3 },
              { texte: "Téléphone et réseaux sociaux", valeur: 2 },
              { texte: "Je me laisse distraire par tout ce qui m'entoure", valeur: 1 }
            ]
          },
          {
            texte: "Étudies-tu plutôt le matin, l'après-midi ou le soir ?",
            type: "choix",
            options: [
              { texte: "Le matin, quand je suis le plus frais(che)", valeur: 3 },
              { texte: "L'après-midi, selon les disponibilités", valeur: 2 },
              { texte: "Le soir, parfois tard", valeur: 1 }
            ]
          }
        ],
        // Catégorie 3: Gestion des pauses et de la motivation
        [
          {
            texte: "Comment prends-tu tes pauses ?",
            type: "choix",
            options: [
              { texte: "Je fais des pauses structurées (ex: technique Pomodoro)", valeur: 3 },
              { texte: "Je prends des pauses aléatoires", valeur: 2 },
              { texte: "Je ne prends pas vraiment de pauses, ou j'en prends trop souvent", valeur: 1 }
            ]
          },
          {
            texte: "Qu'est-ce qui t'aide à rester concentré(e) ?",
            type: "choix",
            options: [
              { texte: "Un environnement calme et une bonne organisation", valeur: 3 },
              { texte: "De la musique ou des bruits de fond", valeur: 2 },
              { texte: "Rien, j'ai du mal à rester concentré(e)", valeur: 1 }
            ]
          },
          {
            texte: "Utilises-tu des outils pour améliorer ta concentration (applications, méthodes de productivité) ?",
            type: "choix",
            options: [
              { texte: "Oui, et ça m'aide beaucoup", valeur: 3 },
              { texte: "J'ai essayé, mais ça ne marche pas toujours", valeur: 2 },
              { texte: "Non, je n'en utilise pas", valeur: 1 }
            ]
          },
          {
            texte: "Lorsque tu perds ta motivation, que fais-tu ?",
            type: "choix",
            options: [
              { texte: "Je fais une pause ou change de tâche temporairement", valeur: 3 },
              { texte: "Je continue avec difficulté", valeur: 2 },
              { texte: "J'abandonne temporairement", valeur: 1 }
            ]
          }
        ],
        // Catégorie 4: Personnalisation et suggestions
        [
          {
            texte: "Quelle fonctionnalité te semblerait la plus utile dans une application d'organisation ?",
            type: "choix",
            options: [
              { texte: "Un planificateur intelligent qui adapte mon emploi du temps", valeur: 7 },
              { texte: "Un gestionnaire de tâches avec rappels", valeur: 6 },
              { texte: "Un outil pour suivre ma concentration et mes performances", valeur: 5 },
              { texte: "Un assistant qui me donne des conseils pour améliorer ma productivité", valeur: 4 }
            ]
          },
          {
            texte: "Si ton niveau de concentration pouvait être évalué en temps réel, comment voudrais-tu que l'application adapte ton environnement de travail ?",
            type: "ouvert",
            options: []
          }
        ]
      ],
      reponses: [],
      valeursConcentration: [],
      currentCategoryIndex: 0,
      currentQuestionIndex: 0,
      reponseOuverte: "",
    };
  },
  computed: {
    currentQuestion() {
      return this.questionsParCategorie[this.currentCategoryIndex][this.currentQuestionIndex];
    },
    totalQuestions() {
      return this.questionsParCategorie.reduce((total, categorie) => total + categorie.length, 0);
    },
    currentQuestionNumber() {
      let count = 1;
      for (let i = 0; i < this.currentCategoryIndex; i++) {
        count += this.questionsParCategorie[i].length;
      }
      return count + this.currentQuestionIndex;
    },
    pourcentage() {
      return ((this.currentQuestionNumber - 1) / this.totalQuestions) * 100;
    }
  },
  methods: {
    navigateToTimeTable() {
      this.showEnvironments = true;
      this.$nextTick(() => {
        if (this.$refs.emploiUpload) {
          this.timetableData = this.$refs.emploiUpload.timetableData;
        }
      });
    },
    toggleView() {
      this.showEnvironments = !this.showEnvironments;
    },
    choisir(reponse, valeur) {
      this.reponses.push({ question: this.currentQuestion.texte, reponse: reponse });
      this.valeursConcentration.push(valeur);
      this.avancerQuestion();
    },
    soumettreReponseOuverte() {
      if (this.reponseOuverte.trim() !== "") {
        this.reponses.push({ 
          question: this.currentQuestion.texte, 
          reponse: this.reponseOuverte 
        });
        this.reponseOuverte = "";
        this.avancerQuestion();
      }
    },
    avancerQuestion() {
      if (this.currentQuestionIndex < this.questionsParCategorie[this.currentCategoryIndex].length - 1) {
        this.currentQuestionIndex++;
      } else if (this.currentCategoryIndex < this.questionsParCategorie.length - 1) {
        this.currentCategoryIndex++;
        this.currentQuestionIndex = 0;
      } else {
        this.termine = true;
        this.analyserReponses();
      }
    },
    analyserReponses() {
      console.log("Analyse des réponses en cours...");
      
      // Utilisation d'axios pour envoyer les données
      axios.post('http://localhost:5000/api/analyser', {
        valeursConcentration: this.valeursConcentration
      })
      .then(response => {
        console.log("Réponse API reçue:", response.data);
        if (response.data && response.data.niveau) {
          this.concentrationLevel = response.data.niveau;
          this.niveauDetecte = response.data.niveau;
          
          // Stocker les détails des scores si disponibles
          if (response.data.scores_details) {
            this.scoreDetails = response.data.scores_details;
          }
        } else {
          console.error("Réponse invalide de l'API:", response.data);
          this.concentrationLevel = "indéterminé";
        }
      })
      .catch(error => {
        console.error("Erreur lors de l'analyse:", error);
        this.concentrationLevel = "erreur";
      });
    },
    recommencer() {
      this.currentCategoryIndex = 0;
      this.currentQuestionIndex = 0;
      this.reponses = [];
      this.valeursConcentration = [];
      this.reponseOuverte = "";
      this.termine = false;
      this.showEnvironments = false;
      this.concentrationLevel = null;
      this.scoreDetails = null;
    }
  }
}
</script>

<style>
/* Styles de base */
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

/* Animation pour l'apparition douce */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Styles du bouton de navigation */
.nav-button {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  background: linear-gradient(to right, #fcc7d3, rgb(211, 168, 252));
  padding: 10px 15px;
  border-radius: 20px;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

/* Container principal du questionnaire */
.questionnaire-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(120deg, rgb(211, 168, 252) 0%, #fcc7d3 50%, rgb(255, 255, 158) 100%);
  padding: 20px;
  margin: 0;
}

/* Panel principal */
.main-panel {
  width: 100%;
  max-width: 650px;
  background-color: rgba(255, 255, 255, 0.92);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #333;
  backdrop-filter: blur(5px);
}

/* Titre principal */
.main-title {
  font-size: 28px;
  font-weight: bold;
  color: rgb(211, 168, 252);
  margin-bottom: 20px;
  text-align: center;
}

/* En-tête de catégorie */
.category-header {
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  padding: 12px 20px;
  border-radius: 15px;
  margin-bottom: 15px;
  color: white;
  box-shadow: 0 4px 12px rgba(211, 168, 252, 0.25);
}

.category-header h2 {
  margin: 0;
  font-size: 18px;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}

/* Barre de progression */
.progress-container {
  width: 100%;
  height: 10px;
  background-color: #f1f2f6;
  border-radius: 10px;
  margin-bottom: 25px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  transition: width 0.5s ease;
}

/* Compteur de questions */
.question-counter {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.question-badge {
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  color: white;
  box-shadow: 0 3px 10px rgba(211, 168, 252, 0.2);
}

.question-total {
  color: rgb(211, 168, 252);
  font-size: 14px;
  font-weight: 500;
}

/* Panel de question */
.question-panel {
  background-color: #fafafa;
  padding: 25px;
  border-radius: 15px;
  margin-bottom: 25px;
  border-left: 4px solid #fcc7d3;
  text-align: left;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.03);
}

.question-panel h2 {
  font-size: 20px;
  font-weight: bold;
  color: rgb(211, 168, 252);
}

/* Conteneur des choix de réponse */
.choices-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

/* Bouton de choix */
.choice-button {
  background-color: white;
  color: #333;
  padding: 16px;
  border-radius: 12px;
  text-align: left;
  border: 1px solid #f1f2f6;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
}

.choice-letter {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, rgb(211, 168, 252), #fcc7d3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-weight: bold;
  color: white;
  box-shadow: 0 2px 5px rgba(211, 168, 252, 0.25);
}

/* Question ouverte */
.open-response {
  margin-top: 20px;
}

.open-textarea {
  width: 100%;
  min-height: 120px;
  padding: 15px;
  border-radius: 12px;
  border: 1px solid rgba(211, 168, 252, 0.3);
  resize: vertical;
  margin-bottom: 15px;
  background-color: white;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.03);
}

.submit-button {
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  padding: 14px 24px;
  border-radius: 12px;
  color: white;
  font-weight: 500;
  cursor: pointer;
  border: none;
  box-shadow: 0 4px 15px rgba(211, 168, 252, 0.25);
  transition: all 0.3s ease;
}

/* Écran de fin */
.completion-screen {
  text-align: center;
}

.completion-circle {
  height: 90px;
  width: 90px;
  background: linear-gradient(135deg, rgb(211, 168, 252), #fcc7d3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 10px 20px rgba(211, 168, 252, 0.2);
}

.completion-circle span {
  font-size: 45px;
  color: white;
}

.completion-title {
  font-size: 28px;
  font-weight: bold;
  color: rgb(211, 168, 252);
  margin-bottom: 15px;
}

.completion-text {
  color: #555;
  margin-bottom: 25px;
  font-size: 16px;
}

.next-steps {
  text-align: left;
  margin-bottom: 25px;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 12px;
  border-left: 4px solid #fcc7d3;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.03);
}

.next-steps h3 {
  color: rgb(211, 168, 252);
  margin-bottom: 10px;
}

.view-environments-button {
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  padding: 14px 24px;
  border-radius: 12px;
  color: white;
  font-weight: 500;
  cursor: pointer;
  border: none;
  box-shadow: 0 4px 15px rgba(211, 168, 252, 0.25);
  transition: all 0.3s ease;
  margin-top: 20px;
}

/* Styles pour le hover des boutons */
button:hover {
  background-color: #fdf6ff !important;
  border-color: rgb(211, 168, 252) !important;
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(211, 168, 252, 0.12) !important;
}

button:active {
  transform: scale(0.98);
}

/* Style pour les textes des boutons au survol */
button:hover span:last-child {
  color: rgb(211, 168, 252);
}

/* Ajout d'un effet arc-en-ciel doux au survol des boutons */
@keyframes softRainbow {
  0% { box-shadow: 0 5px 15px rgba(211, 168, 252, 0.12); }
  33% { box-shadow: 0 5px 15px rgba(252, 199, 211, 0.12); }
  66% { box-shadow: 0 5px 15px rgba(255, 255, 158, 0.12); }
  100% { box-shadow: 0 5px 15px rgba(211, 168, 252, 0.12); }
}

button:hover {
  animation: softRainbow 3s infinite;
}
/* Styles pour le nouvel écran de fin */
.completion-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #f8f8ff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.completion-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #7ee8fa 0%, #80d0c7 100%);
  border-radius: 50%;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
}

.completion-circle span {
  font-size: 2.5rem;
  color: white;
}

.completion-title {
  font-size: 2rem;
  font-weight: 600;
  color: #4a4a4a;
  margin-bottom: 1.5rem;
}

.concentration-result {
  margin: 1.5rem 0;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 1rem;
  width: 100%;
}

.concentration-level {
  font-weight: 700;
  font-size: 1.2rem;
  padding: 0.3rem 0.8rem;
  border-radius: 1rem;
  background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
  color: #3a3a3a;
  display: inline-block;
  margin: 0 0.5rem;
}

.completion-text {
  font-size: 1.1rem;
  color: #666;
  margin: 1rem 0;
}

.start-study-button {
  margin-top: 1.5rem;
  padding: 0.8rem 2rem;
  background: linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%);
  color: white;
  border: none;
  border-radius: 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.start-study-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.start-study-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Styles dynamiques pour les niveaux de concentration */
.concentration-level[data-level="faible"] {
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
}

.concentration-level[data-level="moyen"] {
  background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
}

.concentration-level[data-level="élevé"] {
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
}
</style>
