struct ManageBookTab {
    Table booktable;

    Button addButton;
    Button editButton;
    Button deleteButton;
    Button searchButton;

    TextBox searchBox;
};
void build_manage_book_tab(App& app){

    auto tab = app.createTab("Quan ly sach");

    tab.addButton("Them sach");
    tab.addButton("Cap nhat sach");
    tab.addButton("Xoa sach");

    tab.addTextBox("Tim kiem sach");

    tab.addTable({
        "Ma sach",
        "Ten sach",
        "Tac gia",
        "The loai",
        "So luong",
        "Trang thai"
        
    });
};
