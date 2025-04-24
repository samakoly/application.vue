<template>
  <div class="timetable-wrapper">
    <div class="timetable-container">
      <h1 class="main-title">Planificateur d'Emploi du Temps</h1>
      
      <div class="nav-bar">
        <button @click="clearTimetable" class="action-button">Effacer tout</button>
        <button @click="saveTimetable" class="action-button">Enregistrer</button>
      </div>
      
      <div class="timetable-frame">
        <table class="timetable">
          <thead>
            <tr>
              <th>Jour / Horaire</th>
              <th v-for="time in timeSlots" :key="time">{{ time }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(day, dayIndex) in days" :key="dayIndex">
              <td>{{ day }}</td>
              <td v-for="(time, timeIndex) in timeSlots" :key="timeIndex" :class="{ filled: timetableData[dayIndex][timeIndex].trim() !== '' }">
                <textarea 
                  class="cell-input" 
                  placeholder="Cours..." 
                  v-model="timetableData[dayIndex][timeIndex]"
                  @input="cellChanged(dayIndex, timeIndex)">
                </textarea>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="save-status" :class="{ visible: statusVisible }">{{ statusMessage }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SchoolTimetable',
  data() {
    return {
      days: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
      timeSlots: [
        '08:00-09:00', 
        '09:00-10:00', 
        '10:00-11:00', 
        '11:00-12:00', 
        '12:00-13:00', 
        '13:00-14:00', 
        '14:00-15:00',
        '15:00-16:00',
        '16:00-17:00',
        '17:00-18:00',
        '18:00-19:00'
      ],
      timetableData: [
        ['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '']
      ],
      statusVisible: false,
      statusMessage: 'Emploi du temps enregistré avec succès!'
    }
  },
  mounted() {
    this.loadTimetable();
  },
  methods: {
    cellChanged(dayIndex, timeIndex) {
      // Exemple d'utilisation des paramètres
      const value = this.timetableData[dayIndex][timeIndex];
      if (value.length > 50) {
        this.$set(this.timetableData[dayIndex], timeIndex, value.substring(0, 50));
      }
    },
    saveTimetable() {
      localStorage.setItem('schoolTimetable', JSON.stringify(this.timetableData));
      this.statusMessage = 'Emploi du temps enregistré avec succès!';
      this.showStatus();
    },
    loadTimetable() {
      const savedData = localStorage.getItem('schoolTimetable');
      if (savedData) {
        const parsedData = JSON.parse(savedData);
        
        // Assurer la compatibilité avec les anciennes données si la structure a changé
        if (parsedData.length === this.days.length) {
          // Vérifier si chaque jour a le bon nombre de créneaux horaires
          for (let i = 0; i < parsedData.length; i++) {
            if (parsedData[i].length === this.timeSlots.length) {
              this.timetableData[i] = parsedData[i];
            } else {
              // Ajuster la longueur si nécessaire
              const newRow = [...parsedData[i]];
              while (newRow.length < this.timeSlots.length) {
                newRow.push('');
              }
              this.timetableData[i] = newRow.slice(0, this.timeSlots.length);
            }
          }
        } else {
          // Si le nombre de jours a changé, initialiser avec les données disponibles
          for (let i = 0; i < Math.min(parsedData.length, this.days.length); i++) {
            const newRow = [...parsedData[i]];
            while (newRow.length < this.timeSlots.length) {
              newRow.push('');
            }
            this.timetableData[i] = newRow.slice(0, this.timeSlots.length);
          }
        }
      }
    },
    clearTimetable() {
      if (confirm('Êtes-vous sûr de vouloir effacer tout l\'emploi du temps?')) {
        this.days.forEach((day, dayIndex) => {
          this.timeSlots.forEach((time, timeIndex) => {
            this.$set(this.timetableData[dayIndex], timeIndex, '');
          });
        });
        localStorage.removeItem('schoolTimetable');
        this.statusMessage = 'Emploi du temps effacé!';
        this.showStatus();
      }
    },
    showStatus() {
      this.statusVisible = true;
      setTimeout(() => {
        this.statusVisible = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
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

/* Wrapper pour centrer et ajouter un fond */
.timetable-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: white;
  padding: 20px;
}

/* Container principal */
.timetable-container {
  width: 100%;
  max-width: 1100px;
  background-color: rgba(255, 255, 255, 0.92);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  color: #333;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.6s ease-out;
}

/* Cadre autour du tableau */
.timetable-frame {
  border: 3px solid;
  border-image: linear-gradient(45deg, rgb(211, 168, 252), #fcc7d3, rgb(255, 255, 158)) 1;
  border-radius: 5px;
  padding: 3px;
  margin-bottom: 25px;
  box-shadow: 0 0 20px rgba(211, 168, 252, 0.15);
}

/* Titre principal */
.main-title {
  font-size: 28px;
  font-weight: bold;
  color: rgb(211, 168, 252);
  margin-bottom: 20px;
  text-align: center;
}

/* Barre de navigation */
.nav-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
  align-items: center;
}

/* Boutons */
.action-button {
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  padding: 12px 24px;
  border-radius: 12px;
  color: white;
  font-weight: 500;
  cursor: pointer;
  border: none;
  box-shadow: 0 4px 15px rgba(211, 168, 252, 0.25);
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: scale(1.03);
  box-shadow: 0 5px 15px rgba(211, 168, 252, 0.3);
}

/* Tableau de l'emploi du temps */
.timetable {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.timetable th, .timetable td {
  border: 1px solid #f1f2f6;
  padding: 0;
  text-align: center;
  position: relative;
}

.timetable th {
  background: linear-gradient(to right, rgb(211, 168, 252), #fcc7d3);
  color: white;
  padding: 12px;
  font-weight: 600;
  font-size: 14px;
}

.timetable td:first-child {
  background-color: #fafafa;
  color: rgb(211, 168, 252);
  font-weight: 600;
  padding: 12px;
  font-size: 14px;
}

/* Style spécial pour les jours de weekend */
.timetable tr:nth-child(6) td:first-child,
.timetable tr:nth-child(7) td:first-child {
  background-color: #fff5f8;
  color: #fcc7d3;
}

/* Zone d'édition des cellules */
.cell-input {
  width: 100%;
  height: 100%;
  min-height: 70px;
  padding: 8px;
  border: none;
  background-color: transparent;
  text-align: center;
  font-family: inherit;
  color: #333;
  cursor: pointer;
  resize: none;
  outline: none;
  font-size: 13px;
}

.cell-input:focus {
  background-color: #f9f5ff;
  box-shadow: inset 0 0 0 2px rgb(211, 168, 252);
}

/* Message du statut d'enregistrement */
.save-status {
  text-align: center;
  color: rgb(211, 168, 252);
  font-weight: 500;
  margin-top: 10px;
  height: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.save-status.visible {
  opacity: 1;
}

/* Classes pour les cellules remplies */
.filled {
  background-color: #fdf6ff;
  border-left: 3px solid rgb(211, 168, 252);
}

/* Ajout d'un effet arc-en-ciel doux au survol des boutons */
@keyframes softRainbow {
  0% { box-shadow: 0 5px 15px rgba(211, 168, 252, 0.12); }
  33% { box-shadow: 0 5px 15px rgba(252, 199, 211, 0.12); }
  66% { box-shadow: 0 5px 15px rgba(255, 255, 158, 0.12); }
  100% { box-shadow: 0 5px 15px rgba(211, 168, 252, 0.12); }
}

.action-button:hover {
  animation: softRainbow 3s infinite;
}

/* Pour les écrans plus petits */
@media screen and (max-width: 768px) {
  .timetable-container {
    padding: 15px;
  }
  
  .timetable {
    font-size: 12px;
  }
  
  .cell-input {
    font-size: 11px;
    min-height: 50px;
  }
  
  .action-button {
    padding: 8px 16px;
    font-size: 14px;
  }
}
</style>