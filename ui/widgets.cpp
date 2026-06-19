#pragma once
#include <string>

struct Widget {
    std::string id;

    Widget(const std::string& id)
        : id(id) {}

    virtual void render() = 0;

    virtual ~Widget() = default;
};
