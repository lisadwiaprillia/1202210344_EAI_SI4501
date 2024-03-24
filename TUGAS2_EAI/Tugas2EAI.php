<?php 

$sumber = 'https://apiv3.apifootball.com/?action=get_topscorers&league_id=302&APIkey=2a7fd2061a981d4f736046ec6771a4f0d101797ad2b934668b79dc3a5ddaef8a';
$ubahdata = file_get_contents($sumber);
$decode = json_decode($ubahdata, true);
?>

<!doctype html>
<html>
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" integrity="sha384-dpuaG1suU0eT09tx5plTaGMLBsfDLzUCCUXOY2j/LSvXYuG6Bqs43ALlhIqAJVRb" crossorigin="anonymous">

    <title>Tugas 2 EAI - Consume API</title>

    <style>
        body {
            background-image: url('EAI_Football.jpg'); /* Ganti 'background.jpg' dengan nama gambar Anda */
            background-size: cover; /* Memastikan gambar latar belakang menutupi seluruh halaman */
            background-repeat: no-repeat; /* Mencegah gambar latar belakang diulang */
            background-position: center center; /* Memusatkan gambar latar belakang */
        }
        .container {
            background-color: rgba(255, 255, 255, 0.7); /* Menambahkan lapisan transparan pada konten */
            padding: 20px; /* Menambahkan padding untuk isi konten */
            margin-top: 20px; /* Menambahkan jarak atas agar tidak menempel dengan gambar latar belakang */
            border-radius: 10px; /* Mengatur sudut border */
        }
        .table-container {
            background-color: rgba(255, 255, 255, 0.7); /* Menambahkan lapisan transparan pada tabel */
            padding: 20px; /* Menambahkan padding untuk tabel */
            margin-top: 20px; /* Menambahkan jarak atas agar tidak menempel dengan gambar latar belakang */
            border-radius: 10px; /* Mengatur sudut border */
        }
        .text-white {
            color: white; /* Mengatur warna teks menjadi putih */
            font-weight: bold; /* Mengatur gaya teks menjadi tebal */
        }
    </style>
</head>
<body class="container">
<h4 class="text-center mt-3" style="color: white; font-weight: bold; background-color: rgba(0, 0, 0, 0.5); padding: 10px;">Tugas 2 EAI - Top Score Football</h4>
<h6 class="text-center mt-3" style="color: white; font-weight: bold; background-color: rgba(0, 0, 0, 0.5); padding: 5px;">Lisa Dwi Aprillia | 1202210344 | SI4501</h6>
<div class="table-container container">
    <div class="row">
        <table class="table table-bordered border-primary">
            <thead class="table table-dark">
            <tr>
                <th scope="col" class='text-center'>Player Place</th>
                <th scope="col" class='text-center'>Player Name</th>
                <th scope="col" class='text-center'>Team Name</th>
                <th scope="col" class='text-center'>Goals</th>
                <th scope="col" class='text-center'>Penalty</th>
            </tr>
            </thead>
            <tbody>
            <?php
            foreach ($decode as $value) {
                ?>
                <tr>
                    <td><h6 class='text-center'><?php echo $value['player_place'] ?></h6></td>
                    <td><h6><?php echo $value['player_name'] ?></h6></td>
                    <td><h6><?php echo $value['team_name'] ?></h6></td>
                    <td><h6 class='text-center'><?php echo $value['goals'] ?></h6></td>
                    <td><h6 class='text-center'><?php echo $value['penalty_goals'] ?></h6></td>
                </tr>
                <?php
            }
            ?>
            </tbody>
        </table>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>

</body>
</html>
