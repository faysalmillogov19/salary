// contrat_form.js
document.addEventListener("DOMContentLoaded", function () {
    // Fonction pour masquer ou afficher le champ date_fin en fonction du type de contrat
    function toggleDateFinVisibility() {
        const typeContratField = document.querySelector('.contrat-type');
        const dateFinField = document.querySelector('#id_date_fin');  // Assurez-vous que l'ID correspond à votre modèle

        if (typeContratField.value === 'CDI') {
            dateFinField.style.display = 'none';
        } else {
            dateFinField.style.display = 'block';
        }
    }

    // Appliquer la fonction lors du chargement initial de la page
    toggleDateFinVisibility();

    // Écouter les changements dans le champ type_contrat
    const typeContratField = document.querySelector('.contrat-type');
    typeContratField.addEventListener('change', toggleDateFinVisibility);
});
