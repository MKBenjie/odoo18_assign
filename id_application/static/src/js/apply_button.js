/** @odoo-module **/

import { registry } from "@web/core/registry";

import { Component } from  "@odoo/owl";

import { rpc } from "@web/core/network/rpc";

function ApplicationDashboard(env, options) {
    const container = document.createElement("div");
    container.classList.add("o_centered_content");

    // Fetch applicant data dynamically
    rpc({
        route: "/get_applicant_status",
        params: {},
    })
        .then((response) => {
            container.innerHTML = ""; // Clear initial content

            if (!response.exists) {
                // Display the Apply button
                const applyButton = document.createElement("button");
                applyButton.className = "btn btn-primary btn-lg";
                applyButton.textContent = "Apply";
                applyButton.addEventListener("click", () => {
                    env.services.action.doAction({
                        type: "ir.actions.act_window",
                        res_model: "national.applicant",
                        view_mode: "form",
                        target: "current",
                    });
                });
                container.appendChild(applyButton);
            } else {
                // Display application status
                const statusDiv = document.createElement("div");
                const statusMap = {
                    draft: "Draft",
                    sent: "Sent → Validating",
                    validating: "Validating → Approved",
                    approved: "Approved",
                    denied: "Denied",
                };

                const statusText = statusMap[response.stage] || "Unknown Status";
                statusDiv.innerHTML = `
                    <h2>Your Application Status:</h2>
                    <p class="text-${response.stage}">${statusText}</p>
                `;
                container.appendChild(statusDiv);
            }
        })
        .catch((error) => {
            console.error("Error fetching applicant status:", error);
        });

    document.body.appendChild(container);
}

registry.category("actions").add("id_application.application_dashboard", ApplicationDashboard);