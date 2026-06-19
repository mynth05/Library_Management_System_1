struct ManageBorrowReturnTab {
    Table booktable;

    Button addButton;
    Button editButton;
    Button deleteButton;
    Button searchButton;

    TextBox searchBox;
};
void build_borrow_return_tab(App& app) {

    auto tab = app.createTab("Muon tra");

    tab.addButton("Muon sach");
    tab.addButton("Tra sach");

    tab.addTable({
        "Ma phieu",
        "Ban doc",
        "Sach",
        "Ngay muon",
        "Han tra"
    });
}
