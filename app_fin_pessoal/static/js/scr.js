document.addEventListener('DOMContentLoaded', function() {
    const deleteSelectedBtn = document.querySelector('.delete-selected-btn');
    const deleteCheckboxes = document.querySelectorAll('.delete-checkbox');

    deleteSelectedBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do link

        const selectedIds = [];
        deleteCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedIds.push(checkbox.value);
            }
        });

        if (selectedIds.length > 0) {
            const deleteUrl = `/delete/?ids=${selectedIds.join(',')}`; // Construa a URL com os IDs
            window.location.href = deleteUrl; // Redirecione para a URL de exclusão
        } else {
            alert('Selecione ao menos um registro para apagar.');
        }
    });
});