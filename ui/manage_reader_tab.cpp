struct ManagReaderTab {
    Table readertable;

    Button addButton;
    Button editButton;
    Button deleteButton;
    Button searchButton;

    TextBox searchBox;
};
void build_manage_reader_tab(App& app){

    auto tab = app.createTab("Quan ly ban doc");

    tab.addButton("Them ban doc");
    tab.addButton("Chinh sua thong tin");
    tab.addButton("Xoa ban doc");

    tab.addTextBox("Tim kiem ban doc");

    tab.addTable({
        "Ma ban doc",
        "Ho ten",
        "Ngay sinh",
        "Gioi tinh",
        "Dia chi",
        "So dien thoai"
        
    });
}
