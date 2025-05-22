function my_scope() {
    const forms = document.querySelectorAll(".form_delete");

    for (const form of forms) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const confirm = window.confirm("Are you sure?");

            if (confirm) {
                form.submit();
            }
        });
    }
}

my_scope();
